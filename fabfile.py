"""
Routines for installing whois-bridge on Ubuntu.

To install on a clean Ubuntu Bionic box, simply run
fab bootstrap
"""

from fabric.api import sudo, run, task, env
from fabric.contrib import files

if not env.hosts:
    env.hosts = ['spidey']

install_root = '/opt/whois-bridge'


python = 'python3.8'


@task
def bootstrap():
    install_dependencies()
    install_env()
    install_service()
    update()


@task
def install_dependencies():
    sudo('apt install -y software-properties-common')
    sudo('add-apt-repository -y ppa:deadsnakes/ppa')
    sudo('apt update -y')
    sudo(f'apt install -y {python} {python}-venv')


@task
def install_env():
    user = run('whoami')
    sudo(f'rm -R {install_root} || echo -n')
    sudo(f'mkdir -p {install_root}')
    sudo(f'chown {user} {install_root}')
    run(f'{python} -m venv {install_root}')
    run(f'{install_root}/bin/python -m pip install -U pip')


@task
def install_service():
    files.upload_template(
        "ubuntu/whois-bridge.service",
        "/etc/systemd/system",
        use_sudo=True,
        context=globals(),
    )
    sudo('systemctl enable whois-bridge')


@task
def update():
    install()
    sudo('systemctl restart whois-bridge')


def install():
    """
    Install jaraco.net to environment at root.
    """
    run('git clone https://github.com/jaraco/jaraco.net || echo -n')
    run('git -C jaraco.net pull')
    run(f'{install_root}/bin/python -m pip install -U ./jaraco.net')


@task
def remove_all():
    sudo('stop whois-bridge || echo -n')
    sudo('rm /etc/systemd/system/whois-bridge.service || echo -n')
    sudo('rm -Rf /opt/whois-bridge')
