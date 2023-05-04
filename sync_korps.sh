# This script manually syncs korp.csc.fi to korp2.csc.fi
# Assumptions:
# - korp.csc.fi contains the master data
# - root's .ssh/authorized_keys file on both servers allows for passwordless login
# - SSH Agent Forwarding is active on korp.csc.fi and localhost

# Method: ssh to korp.csc.fi as root and start rsync to root@korp2 using the
# forwarded local credentials

# to run: sync_korps.sh

ssh root@korp.csc.fi rsync -av --delete                      /var/www/html/download korp2.csc.fi:/data2
ssh root@korp.csc.fi rsync -av --delete --exclude korp/cache /mnt/cwbdata           korp2.csc.fi:/data1
