"""
Routines for installing whois-bridge on Ubuntu.

To install on a clean Ubuntu Bionic box, simply run
fab bootstrap
"""

from fabric import task
from jaraco.fabric import files

hosts = ['spidey']

install_root = '/opt/whois-bridge'


python = 'python3.8'


@task(hosts=hosts)
def bootstrap(c):
    install_dependencies(c)
    install_env(c)
    install_service(c)
    update(c)


@task
def install_dependencies(c):
    c.sudo('apt install -y software-properties-common')
    c.sudo('add-apt-repository -y ppa:deadsnakes/ppa')
    c.sudo('apt update -y')
    c.sudo(f'apt install -y {python} {python}-venv')


@task
def install_env(c):
    user = c.run('whoami')
    c.sudo(f'rm -R {install_root} || echo -n')
    c.sudo(f'mkdir -p {install_root}')
    c.sudo(f'chown {user} {install_root}')
    c.run(f'{python} -m venv {install_root}')
    c.run(f'{install_root}/bin/python -m pip install -U pip')


@task
def install_service(c):
    files.upload_template(
        c,
        "ubuntu/whois-bridge.service",
        "/etc/systemd/system",
        context=globals(),
    )
    c.sudo('systemctl enable whois-bridge')


@task
def update(c):
    install(c)
    c.sudo('systemctl restart whois-bridge')


def install(c):
    """
    Install jaraco.net to environment at root.
    """
    c.run('git clone https://github.com/jaraco/jaraco.net || echo -n')
    c.run('git -C jaraco.net pull')
    c.run(f'{install_root}/bin/python -m pip install -U ./jaraco.net')


@task
def remove_all(c):
    c.sudo('stop whois-bridge || echo -n')
    c.sudo('rm /etc/systemd/system/whois-bridge.service || echo -n')
    c.sudo('rm -Rf /opt/whois-bridge')
