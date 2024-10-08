#!/usr/bin/env python3
# -*- mode: Python; -*-

# A simple authentication and authorization database management tool
# to support Korp configuration with CLARIN access classes; to go with
# an auth.cgi in backend/korp/.
# By Jussi Piitulainen, jpiitula@ling.helsinki.fi, for
# FIN-CLARIN, December 2013.
# Updated for Python3 by Sam Hardwick, September 2024.


import MySQLdb
import sys, codecs, re

import korp_authdb_config as auth_config


class ArgumentError(Exception):
    """Exception raised on invalid arguments"""

    pass


def usage_command(cursor, command, args):
    print(
        """\
Usage: {prog} command [arg ...]

The arguments in the command descriptions below are as follows:
  PERSON: the Shibboleth (Haka) user name (username@domain)
  CORPUS: the Korp corpus id (Corpus Workbench name of a corpus)
  URN@LBR: the LBR id of the corpus: the corpus URN suffixed with "@LBR"

Korp corpus ids are upper-cased and LBR ids are prefixed with
"urn:nbn:fi:lb-" and suffixed with "@LBR" if they are missing.

Available commands and their arguments:

  PUB CORPUS ...        make corpora PUB
  ACA CORPUS ...        make corpora ACA
  RES CORPUS ...        make corpora RES
    Note: ACA and RES corpora also need appropriate settings in the Korp
    frontend corpus configuration.

  lbr_register URN@LBR CORPUS ...
                        map LBR id to Korp corpus ids
  lbr_unregister URN@LBR CORPUS ...
                        unmap LBR id and Korp corpus ids
  lbr_map               show LBR id mappings

  persons               list persons
  corpora               list corpora and their licenses

  allow PERSON [PERSON ... --] CORPUS ...
                        give persons personal access to corpora
  deny PERSON [PERSON ... --] CORPUS ...
                        take away from persons personal access to corpora
    Note: If you specify multiple PERSONs, the CORPUS ids need to be
    separated from them by a double dash "--".

DEPRECATED, DO NOT USE:
  remove PERSON ...     remove persons (idempotent)
    """.format(
            prog=sys.argv[0]
        )
    )


def remove_command(cursor, command, args):
    """Remove person"""
    (person,) = args
    cursor.execute(
        """
    delete from auth_academic where person = %s""",
        [person],
    )
    cursor.execute(
        """
    delete from auth_allow where person = %s""",
        [person],
    )
    cursor.execute(
        """
    delete from auth_secret where person = %s""",
        [person],
    )


def allow_command(cursor, command, args):
    """Give person personal access to corpus"""
    person, corpus = args
    cursor.execute(
        """
    insert into auth_allow(person, corpus)
    values (%s, %s)
    on duplicate key
    update corpus = corpus""",
        [person, corpus],
    )


def deny_command(cursor, command, args):
    """Take away personal access to corpus from person"""
    person, corpus = args
    cursor.execute(
        """
    delete from auth_allow
    where person = %s and corpus = %s""",
        [person, corpus],
    )


def lbr_register_command(cursor, command, args):
    """Map a LBR URN ID to one or more (sub)coropra"""
    lbr_id, corpus = args
    cursor.execute(
        """
    insert into auth_lbr_map(lbr_id, corpus)
    values (%s, %s)
    on duplicate key
    update corpus = corpus""",
        [lbr_id, corpus],
    )


def lbr_unregister_command(cursoer, command, args):
    """Map a LBR URN ID to one or more (sub)coropra"""
    lbr_id, corpus = args
    cursor.execute(
        """
    delete from auth_lbr_map
    where lbr_id = %s and corpus = %s""",
        [lbr_id, corpus],
    )


def license_command(cursor, command, args):
    """Make corpus be of given type (PUB, ACA, or RES)"""
    license = command
    (corpus,) = args
    cursor.execute(
        """
    insert into auth_license(corpus, license)
    values (%s, %s)
    on duplicate key
    update license = %s""",
        [corpus, license, license],
    )
    # Disabled because not currently working well
    # check_config(corpus, license)


def persons_command(cursor, command, args):
    """List persons and their personally allowed corpora"""
    cursor.execute(
        """
    (select distinct person from auth_allow)
        order by person"""
    )
    for (person,) in cursor.fetchall():
        print(person, end="")
        cursor.execute(
            """
        select corpus from auth_allow
        where person = %s
        order by corpus""",
            [person],
        )
        for corpus in cursor:
            print(" ", corpus[0], end="")
        print()


def corpora_command(cursor, command, args):
    """List corpora, their license (PUB, ACA, or RES), and their corporal
    persons (persons allowed personal access to the corpus)"""
    cursor.execute(
        """
    select corpus, license from auth_license
    order by corpus"""
    )
    for corpus, license in cursor.fetchall():
        print(corpus, license, end="")
        cursor.execute(
            """
        select person from auth_allow
        where corpus = %s
        order by person""",
            [corpus],
        )
        for (person,) in cursor:
            print("", person, end="")
        print()
        # Disabled because not currently working well
        # check_config(corpus, license)


def lbr_map_command(cursor, command, args):
    """List URN@LBR-IDs and Korp-ID mappings"""
    cursor.execute(
        """
    select lbr_id, corpus from auth_lbr_map
    order by lbr_id"""
    )
    for lbr_id, corpus in cursor.fetchall():
        print("%s\t%s" % (lbr_id, corpus))


def check_corpus_arg(corpus):
    """Check a corpus argument and convert it to upper case"""
    corpus = corpus.upper()
    if not re.match(r"^[_A-Z][_A-Z0-9-]*$", corpus):
        print('Warning: Invalid corpus id "{}"; skipping'.format(corpus))
        return None
    return corpus


def check_lbr_id_arg(lbr_id):
    """Check an LBR id argument and augment it if needed"""
    # Note: This assumes that LBR ids are of the form
    # "urn:nbn:fi:lb-NUMBER@LBR". If they are changed to something else, this
    # will have to be modified accordingly.
    if not re.match(r"^((urn:nbn:fi:)?lb-)?\d+(@LBR)?", lbr_id):
        print('Warning: Invalid LBR id "{}"; skipping'.format(lbr_id))
        return None
    if not lbr_id.endswith("@LBR"):
        lbr_id += "@LBR"
    if not lbr_id.startswith("urn:"):
        if not lbr_id.startswith("lb-"):
            lbr_id = "lb-" + lbr_id
        lbr_id = "urn:nbn:fi:" + lbr_id
    return lbr_id


def check_person_arg(person):
    """Check a person (username) argument"""
    if not re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_.-]+", person):
        print('Warning: Possibly invalid username "{}"'.format(person))
    return person


# Values in dispatch are triples (command function, argument list split type,
# argument types); see parse_arglist below for argument list split types.
dispatch = dict(
    remove=(remove_command, "+", "p"),
    allow=(allow_command, "++", "pc"),
    deny=(deny_command, "++", "pc"),
    PUB=(license_command, "+", "c"),
    ACA=(license_command, "+", "c"),
    RES=(license_command, "+", "c"),
    persons=(persons_command, "", ""),
    corpora=(corpora_command, "", ""),
    lbr_register=(lbr_register_command, "1+", "lc"),
    lbr_unregister=(lbr_unregister_command, "1+", "lc"),
    lbr_map=(lbr_map_command, "", ""),
    help=(usage_command, "", ""),
)

arg_checker = dict(c=check_corpus_arg, l=check_lbr_id_arg, p=check_person_arg)


def check_config(corpus, license):
    """Reports on possible incompatibilities with frontend config files.
    Note! This does not cover all possibilities - if something is not
    found, the problems may well be in this function instead of in the
    config files."""

    found_containing = []
    for config in auth_config.KORP_CONFIG:
        text = codecs.open(config, "r", "utf-8").read()
        matches = re.findall(
            r"\bsettings.corpora.%s\s*=\s*[{].*?[{}]" % corpus.lower(),
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if len(matches) > 0:
            found_containing.append(config)

        if len(matches) > 1:
            print("! %s: found many in %s" % (corpus, config))

        for match in matches:
            limitations = re.findall(
                r"\blimited_access\s*:\s*(\w+)", match, re.MULTILINE | re.DOTALL
            )
            if len(limitations) > 1:
                print("! %s: multiply limited in %s" % (corpus, config))

            if license in ("ACA", "RES") and not limitations:
                print("! %s: missing limitation in %s" % (corpus, config))

            if license in ("ACA", "RES"):
                for limitation in limitations:
                    if limitation == "false":
                        print(
                            "! %s: incompatible non-limitation in %s" % (corpus, config)
                        )
            else:
                for limitation in limitations:
                    if limitation == "true":
                        print("! %s: incompatible limitation in %s" % (corpus, config))

    if len(found_containing) == 0:
        print("! %s: not found in any config file" % corpus)

    if len(found_containing) > 1:
        print(
            "! %s: found in more than one config file: %s"
            % (corpus, " ".join(found_containing))
        )


def parse_arglist(args, split_type):
    """Split list args into a pair of lists according to split_type.

    split_type can be one of the following:
      '' (or any other False-like): no args used
      '+': all args to the first list
      '1+': first arg to the first list, the rest to the second
      '++': if args contains '--', args before it to the first list,
            the rest to the second; otherwise like '1+'
    If a list in the returned pair gets no arguments, its value will
    be [None].
    args must have at least len(split_type) items.
    """
    if not split_type:
        return ([None], [None])
    elif split_type == "+":
        return (args, [None])
    elif split_type == "1+":
        return ([args[0]], args[1:])
    elif split_type == "++":
        try:
            sep_idx = args.index("--")
            return (args[:sep_idx], args[sep_idx + 1 :])
        except ValueError:
            return ([args[0]], args[1:])


def do_dispatch(cursor, args):
    """Dispatch command function based on args, passing cursor.

    args contains the command and its arguments. The arguments are
    split as the command expects and the command function is called as
    many times as needed.
    """
    if len(args) == 0:
        raise ArgumentError("No command given")
    command, args = args[0], args[1:]
    dispatch_func, dispatch_argsplit, dispatch_argtypes = dispatch.get(
        command, (None, "", "")
    )
    if dispatch_func is None:
        raise ArgumentError('Unrecognized command "{}"'.format(command))
    if not dispatch_argsplit:
        # No arguments needed
        if args:
            print(
                '{}: Warning: Spurious arguments to command "{}"'.format(
                    sys.argv[0], command
                )
            )
        dispatch_func(cursor, command, ())
    else:
        if len(args) < len(dispatch_argsplit):
            raise ArgumentError(
                'Command "{}" requires at least {:d} argument{}'.format(
                    command,
                    len(dispatch_argsplit),
                    "s" if len(dispatch_argsplit) > 1 else "",
                )
            )
        parsed_args = parse_arglist(args, dispatch_argsplit)
        for arg1 in parsed_args[0]:
            arg1 = arg_checker[dispatch_argtypes[0]](arg1)
            if arg1 is None:
                continue
            for arg2 in parsed_args[1]:
                # Pass only the non-None arguments, so that they are unpacked
                # correctly in the command functions
                if len(dispatch_argtypes) > 1:
                    arg2 = arg_checker[dispatch_argtypes[1]](arg2)
                    if arg2 is None:
                        continue
                dispatch_args = tuple(arg for arg in [arg1, arg2] if arg)
                # print(command, dispatch_args)
                try:
                    dispatch_func(cursor, command, dispatch_args)
                except MySQLdb.IntegrityError as e:
                    # Does this cover all cases?
                    if "REFERENCES `auth_license`" in str(e):
                        print(
                            '{}: Error: License for corpus "{}" has not been'
                            " specified".format(sys.argv[0], arg2)
                        )


if __name__ == "__main__":
    conn = MySQLdb.connect(use_unicode=True, **auth_config.DBCONNECT)
    try:
        cursor = conn.cursor()
        do_dispatch(cursor, sys.argv[1:])
        cursor.close()
        conn.commit()
    except ArgumentError as e:
        print("{}: Error:".format(sys.argv[0]), e)
        print('Try "{prog} help" for usage'.format(prog=sys.argv[0]))
    except MySQLdb.MySQLError:
        import traceback

        # Do not show calls in libraries
        traceback.print_exc(3)
        print()
        print('Try "{prog} help" for usage'.format(prog=sys.argv[0]))
