# Logging

There are three server applications that in theory can write logs on Korp:

1. `korp.py`, ie. the Korp backend
2. `korp-auth.py`, an authoritization checking server
3. `korp_download.cgi` and `korp.cgi`, legacy cgi programs that handle
   downloading the results of queries

`korp.py` and `korp-auth.py` are configured to write logs to syslog,
`/dev/log`. A syslog service called `rsyslog` is configured on the
Korp machine to write their logs to `/var/log/korp/` as `korp.log` and
`korp-auth.log`, respectively. rsyslog is also capable of forwarding
the logs to an external log consumer. See
`/etc/rsyslog.d/11-korp-py.conf`.

`korp_download.cgi` and `korp.cgi` write logs in the old-fashioned way
(without any protection against simultaneous writes) to files in
`/v/korp/log`. If this situation persists for a long time, we could
consider handling their logs with syslog too.

All these logs are currently being rotated monthly and deleted after
15 months.
