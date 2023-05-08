# The Language Bank Korp Instance Provisioning

## Prerequisites

- Ansible >=2.5: https://docs.ansible.com/ansible/latest/installation_guide/index.html
- Python 3: Needed by the OpenStack command line tools
- [Access to Pouta](https://docs.csc.fi/accounts/how-to-add-service-access-for-project/)
- Your cPouta project's [OpenStack RC file](https://docs.csc.fi/cloud/pouta/install-client/#configure-your-terminal-environment-for-openstack)
- Key pair for cPouta instances. Created in https://pouta.csc.fi/ (Project > Compute > Key Pairs) and must be named "kielipouta".

## Install requirements
For Python requirements, it is recommended to use a virtual environment:
```
virtualenv .venv -p python3
source .venv/bin/activate
pip install -r requirements_dev.txt
```

The activation step must be done separately for each new session.

After that, external ansible roles can be installed via
```
ansible-galaxy install -r requirements.yml
```

## Source your cPouta (OpenStack) auth file.

The [OpenStack auth file](https://docs.csc.fi/#cloud/pouta/install-client/#configure-your-terminal-environment-for-openstack) is necessary for provisioning the OpenStack resources. 

```
$ source project_2000680-openrc.sh
```

## Making sure that SSH connection to korp2 works

To ensure that you can establish an SSH connection from your local machine to korp2 from outside the office network (VPN still needed), add the following entries to your `.ssh/config`:

```
host korp.csc.fi
  HostName korp.csc.fi
  ForwardAgent yes
  User cloud-user
  IdentityFile ~/.ssh/id_rsa

host korp2.csc.fi
  HostName korp2.csc.fi
  ProxyJump korp.csc.fi
  User cloud-user
```

Modify the `IdentityFile` path if needed. Establishing a connection to korp2.csc.fi should now work via korp.csc.fi (i.e. the playbook should run without issues).


## Provisioning

Run the provisioning playbook.

```
$  ansible-playbook site.yml -i inventories/korp2
```

By default, some files are downloaded locally into `~/Downloads`. If you do not
wish to use that directory, specify an alternative using `--extra-vars
"local_download_dir=your/path/here"`.
