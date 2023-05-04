#!/usr/bin/env perl
#
# Version: $Id$
#
use strict;
use warnings;
use CGI;
use CGI::Carp qw( fatalsToBrowser);
use URI;

#
# constants
#
my @ATTRIBUTES_REQUIRED = qw(
    eduPersonPrincipalName:eppn
);
my @ATTRIBUTES_OPTIONAL = qw(
    eduPersonUnScopedAffiliation:unscoped_affiliation:eduPersonAffiliation
    eduPersonEntitlement:entitlement
);


# allow override from environment ...
if (exists $ENV{'SHIBTEST_ATTRIBUTES_REQUIRED'}) {
    @ATTRIBUTES_REQUIRED = split('\s+', $ENV{'SHIBTEST_ATTRIBUTES_REQUIRED'});
}
if (exists $ENV{'SHIBTEST_ATTRIBUTES_OPTIONAL'}) {
    @ATTRIBUTES_OPTIONAL = split('\s+', $ENV{'SHIBTEST_ATTRIBUTES_OPTIONAL'});
}


#
# code below ... nothing to change there ...
#
sub xml_escape {
    my $s = shift;

    $s =~ s!&!&amp;!gs;
    $s =~ s!<!&lt;!gs;
    $s =~ s!>!&gt;!gs;
    return $s;
}


sub render_table_rows {
    my $caption = shift;
    my $keys    = shift;
    my $i = 0;
    print '<tr class="header">', '<th colspan="2">',
        $caption, '</th>', '</tr>';
    if (scalar(@{$keys}) > 0) {
	foreach my $key (@{$keys}) {
	    my $value = $ENV{$key};
	    $value =~ s!\n*!!gs;
	    $value =~ s!\s*(;|\$)\s*!\n!gs;
	    $value = xml_escape($value);
	    $value =~ s!\n!<br />!gs;
	    print '<tr class="', ($i++ % 2 == 0 ? 'even' : 'odd'), '">';
	    print '<td>', $key, '</td>', '<td>', $value, '</td>', '</tr>';
	}
    }
    else {
	print '<tr class="even"><td colspan="2">',
            '<span class="error center">[NONE]</span></tr>';
    }
}


sub dump_shibboleth_attributes {
    my $debug_env = shift;
    
    my @keys = sort(keys(%ENV));
    my @attrs = grep(!m/^(HTTPS|SERVER_|SCRIPT_|PATH|QUERY_STRING|GATEWAY|DOCUMENT_ROOT|REMOTE|REQUEST|HTTP_|AUTH_TYPE|Shib_)/i, @keys);
    my @shib = grep(m/Shib_/i, @keys);

    render_table_rows('Shibboleth Attributes:', \@attrs);
    render_table_rows('Shibboleth Enviroment Variables:', \@shib);
    if (defined ($debug_env)) {
        render_table_rows('All Environment Variables:', \@keys);
    }
}


sub dump_shibboleth_assertions {
    my $count = shift;

    return unless defined($count) && $count > 0;

    # try to load LWP and XML::Twig and bail if not available ...
    eval {
	require LWP;
	require XML::Twig;
    };
    if ($@) {
	return;
    }
    print '<tr class="header">', '<th colspan="2">',
        'Raw SAML Assertion(s)', '</th>', '</tr>';
    my $j = 0;
    my $browser = LWP::UserAgent->new;
    ASSERTION:
    for (my $i = 1; $i <= $count; $i++) {
        my $url = $ENV{sprintf('Shib_Assertion_%02d', $i)};
        next ASSERTION unless defined ($url);

	print '<tr class="', ($j++ % 2 == 0 ? 'even' : 'odd'), '">';
        print '<td>Assertion ', $i, '</td>';
        my $response = $browser->get($url);
        if ($response->is_success) {
	    my $twig = XML::Twig->new(pretty_print => 'indented',
				      output_encoding => 'utf-8',
				      no_prolog => '1',
				      keep_original_prefix => '1');
	    $twig->parse($response->content);
	    my $s = $twig->sprint();
	    $s = xml_escape($s);
	    $s =~ s! !&nbsp;!gs;
	    $s =~ s!\n!<br />!gs;
	    print '<td>', $s, '</td>';
        }
        else {
	    print '<td>', '<span class="error">Cannot retieve assertion: ',
	    xml_escape($response->status_line), '</span>', '</td>';
        }
	print '</tr>';
    }
}


sub make_self_uri {
    my $scheme = exists $ENV{'HTTPS'} ? 'https' : 'http';
    my $uri = URI->new($scheme . '://' . $ENV{'SERVER_NAME'});
    $uri->path($ENV{'REQUEST_URI'});
    return $uri->as_string();
}


sub make_shibboleth_uri {
    my $path = shift;

    # XXX: always assume https for Shibboleth URIs ...
    my $uri = URI->new('https://' . $ENV{'SERVER_NAME'});
    $uri->path($path);
    return $uri;
}


sub make_login_uri {
    my $uri = $ENV{'SHIBTEST_LOGIN_URI'};
    if (defined($uri)) {
	$uri = URI->new($uri);
    }
    else {
	$uri = make_shibboleth_uri('/Shibboleth.sso/Login');
    }
    $uri->query_form({
	target => make_self_uri(),
    });
    return $uri->as_string();
}


sub make_logout_uri {
    my $uri = $ENV{'SHIBTEST_LOGOUT_URI'};
    if (defined($uri)) {
	$uri = URI->new($uri);
    }
    else {
	$uri = make_shibboleth_uri('/Shibboleth.sso/Logout');
    }
    $uri->query_form({
	return => make_self_uri(),
    });
    return $uri->as_string();
}


sub scan_attributes {
    my $scan_ref    = shift;
    my $optional    = shift;
    my $missing     = 0;

    foreach my $aliases (@{$scan_ref}) {
	my $found = undef;
	my @attrs = split(':', $aliases);

        KEY:
	foreach my $b (keys(%ENV)) {
	    foreach my $a (@attrs) {
		if (lc($a) eq lc($b)) {
		    $found = $b;
		    last KEY;
		}
	    }
	}

	if (defined($found)) {
	    print '<p class="attr ok">',
                ($optional ? 'Optional'
                           : 'Required'),
                ' attribute <code>', $attrs[0], '</code> is available',
                ($found ne $attrs[0] ? " (exported as <code>$found</code>)"
                                     : ''),
		'.</p>';
	}
	else {
	    print '', ($optional ? '<p class="attr warn">Optional'
                                 : '<p class="attr error">Required'),
		' attribute <code>', $attrs[0],
                '</code> is not available.</p>';
	    $missing++;
	}
    }
    return $missing;
}


sub main {
    my $q = shift;

    if (defined($ENV{'Shib_Session_ID'})) {
	# logout link
	my $idp = $ENV{'Shib_Identity_Provider'};
	if (!defined($idp)) {
	    $idp = '<span class="error">[UNKNOWN]</span>';
	}
	print '<p>';
	print 'A Shibboleth session was established with <em>', $idp,
            '</em>.';
        if (defined($ENV{'SHIBTEST_LAZY'})) {
            print ' [<a href="', make_logout_uri(), '">Logout</a>]<br />';
            print 'NB: if this webserver is configured to always requires ',
                'authentication for this page, you will be immediately ',
                'redirected to the WAYF/Discovery service after logging out!';
        }
	print '</p>';

	my $errors   = 0;
	my $warnings = 0;
	# CLARIN required attributes
	if (scalar(@ATTRIBUTES_REQUIRED) > 0) {
	    $errors += scan_attributes(\@ATTRIBUTES_REQUIRED, 0);
	}

	# CLARIN optional attributes
	if (scalar(@ATTRIBUTES_OPTIONAL) > 0) {
	    $warnings += scan_attributes(\@ATTRIBUTES_OPTIONAL, 1);
	}

	# remote user
	my $user = $ENV{'REMOTE_USER'};
	$warnings++ unless defined($user);
	print '<p class="attr ', (defined($user) ? 'ok' : 'warn'), '">';
	print 'REMOTE_USER: ',
            (defined($user) ? $user : 'N/A (not exported by mod_shib?!)');
	print '</p>';

	if ($errors == 0) {
	    print '<p class="ok result">Interoperability between your SP ',
                'and the IDP is ',
                ($warnings > 0 ? 'sufficent' : 'optimal'), '. ',
                $errors, ' error(s), ',
                $warnings, ' warning(s)</p>';
	}
	else {
	    print '<p class="error result">Interoperability between your SP ',
	        'and the IDP is problematic! ', $errors, ' error(s), ',
                $warnings, ' warning(s) <br/>',
	        'Please check SP config and IDP release policy.</p>';
	}
	# attribute / environment variable / assertion
	print '<table class="attr">';
	my $debug_env = (defined($q) && $q->param('debug_env'));
	dump_shibboleth_attributes($debug_env);
	dump_shibboleth_assertions($ENV{'Shib_Assertion_Count'});
	print '</table>';
    }
    else {
	# login link
	print '<p>No Shibboleth session exists, please <a href="',
            make_login_uri(), '">Login</a>.</p>';
    }
}


my $style = <<STYLE;
body {
    font-family: Arial, Verdana, sans-serif;
    font-size: 12pt;
    margin: 0;
    padding: 2px;
}

h1 {
    font-size: 150%;
    margin: 0 0 5px 0;
    padding: 0;
}

h2 {
    font-size: 100%;
    margin: 1px 0;
    padding: 0;
}

p {
    margin: 10px 0;
    padding: 4px;
}

p.ok {
    color: #FFFFFF;
    background-color: #009900;
}


p.warn {
    color: #000000;
    background-color: #FFFF00;
}

p.error {
    color: #FFFFFF;
    background-color: #CC0000;
    font-weight: bold;
}

p.attr {
    margin: 1px 0;
}

p.result {
    margin: 20px 0;
    font-size: 120%;
    font-weight: bold;
    border: 2px solid #000000;
}

code {
    font-family: "Courier New", monospace;
    font-weight: bold;
}

span.error {
    color: #CC0000;
    background-color: inherit;
    font-weight: bold;
}

table {
    border: 1px solid #000000;
    border-collapse: collapse;
    margin: 0;
    padding: 0;
}

td, th {
    border: 1px solid #000000;
    vertical-align: top;
    text-align: left;
    margin: 0;
    padding: 4px;
}

th {
    font-weight: bold;
    font-size: 110%;
    color: #FFFFFF;
    background-color: transparent;
}

.header {
    color: inherit;
    background-color: #707677;
}

.even {
    color: inherit;
    background-color: #E7E7E7;
}

.odd {
    color: inherit;
    background-color: #CFCFCF;
}
STYLE

my $q = CGI->new();
print $q->header(-type => 'text/html', -charset => 'utf-8');
print $q->start_html(-title => 'CLARIN SPF Interoperability Test Page',
		     -style => { -code => $style });
print $q->h1('CLARIN SPF Interoperability Test Page');
main($q);
print $q->end_html;
exit 0;
