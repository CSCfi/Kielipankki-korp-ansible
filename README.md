# The Language Bank Korp Instance Provisioning

# Prerequisites

For running the Ansible playbook, the prerequisites are largely the same as
with the other servers. See e.g. [proxy README](../kielipankki-proxy/README.md)
for details.


# Provisioning

Run the provisioning playbook.

`$  ansible-playbook site.yml -i inventories/korp2`

By default, some files are downloaded locally into `~/Downloads`. If you do not
wish to use that directory, specify an alternative using `--extra-vars
"local_download_dir=your/path/here"`.
