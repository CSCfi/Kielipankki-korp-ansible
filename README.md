# The Language Bank's Korp management

## Prerequisites

- Ansible >=2.5: https://docs.ansible.com/ansible/latest/installation_guide/index.html
- Python 3: Needed by the OpenStack command line tools
- [Access to Pouta](https://docs.csc.fi/accounts/how-to-add-service-access-for-project/)
- Your cPouta project's [OpenStack RC file](https://docs.csc.fi/cloud/pouta/install-client/#configure-your-terminal-environment-for-openstack)
- Key pair for cPouta instances. Created in https://pouta.csc.fi/ (Project > Compute > Key Pairs) and must be named "kielipouta".

### Install requirements
For Python requirements, it is recommended to use a virtual environment:
```bash
virtualenv .venv -p python3
source .venv/bin/activate
pip install -r requirements_dev.txt
```

The activation step must be done separately for each new session.

After that, external ansible roles can be installed via
```bash
ansible-galaxy install -r requirements.yml
```

### Source your cPouta (OpenStack) auth file.

The [OpenStack auth file](https://docs.csc.fi/#cloud/pouta/install-client/#configure-your-terminal-environment-for-openstack) is necessary for provisioning the OpenStack resources.

```bash
source project_2000680-openrc.sh
```

That is correct for the production instance, but note that some instances may be running on a different project, like `clarin`.

### SSH access to Korp

You will need to be able to connect via `ssh` to the Korp instance you are provisioning (see `inventories/`). Generally this requires connecting via VPN or the office network, and using a key that has already been installed there by someone else. If you are provisining a fresh Pouta instance, you can install any keys you like by editing `pouta-vm.yml`

## Provisioning an instance

### Development instance

The development instance is created on Pouta and uses a local database. No corpora are included out of the box.

```bash
ansible-playbook korp-pouta.yml -i inventories/dev/hosts
```

Accessing a newly created instance requires updating the IP in (pre-prod) proxy settings: see [proxy repo](https://github.com/cscfi/kielipankki-proxy?tab=readme-ov-file#updating-ips-of-proxied-vms-like-portal-webanno-etc) for more details.

### Production instance

Run the provisioning playbook.

```bash
ansible-playbook korp-production.yml -i inventories/prod/hosts
```

By default, some files are downloaded locally into `~/Downloads`. If you do not
wish to use that directory, specify an alternative using `--extra-vars
"local_download_dir=your/path/here"`.

### Recompilation of frontend

The script will recompile the frontend in case of changes (including new news). You can force the recompilation and reinstallation of the frontend using
the `force_compile` parameter, e.g.:

$ ansible-playbook -vi inventories/prod/hosts korp-production.yml -t korp-frontend -e force_compile=true

### Install only new news

To just update the news information you can start later in the script:

$ ansible-playbook -vi inventories/prod/hosts korp-production.yml -t korp-frontend --start-at="update worktrees" -e force_compile=true

### Update only autoindex for Download

To only update the autoindex file creating the links in "/download" run

$ ansible-playbook -vi inventories/prod/hosts korp-production.yml -t download_autoindex
