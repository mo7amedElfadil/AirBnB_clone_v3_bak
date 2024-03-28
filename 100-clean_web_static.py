#!/usr/bin/python3
"""
Fabric script that creates and distributes
an archive to my web servers,
using the function deploy
"""
from os.path import basename, exists, splitext
from fabric.api import local, env, run, put, runs_once, cd, task
from datetime import datetime
from os.path import getsize

env.hosts = ["18.234.145.137", "54.196.49.246"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


@runs_once
def do_pack():
    """Packs the web_static files into .tgz file"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(file))
    local("mkdir -p versions")
    if local("tar -cvzf {} web_static".format(file)).succeeded:
        print("web_static packed: {} -> {}Bytes".format(file, getsize(file)))
        return file
    return None


@task
def do_deploy(archive_path):
    """Deploys the archive to the web servers
    usage:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/web_static_20240306225407.tgz
    -i my_ssh_private_key -u ubuntu
    """
    try:
        if not exists(archive_path):
            return False

        target = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        archive_path = basename(archive_path)
        file, _ = splitext(archive_path)

        with cd(target):
            run("mkdir -p {}".format(file))
            run("tar -xzf /tmp/{} -C {}".format(archive_path, file))
            run("mv {}/web_static/* {} && rm -rf {}/web_static"
                .format(file, file, file))

        run("rm /tmp/{}".format(archive_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(target, file))

        print("New version deployed!")

    except Exception:
        return False

    return True


@task
def deploy():
    """ Creates and distributes an archive to the web servers
        usage: fab -f 3-deploy_web_static.py deploy
    """
    try:
        archive_path = do_pack()
        if archive_path is None:
            return False
        return do_deploy(archive_path)
    except Exception:
        return False


@runs_once
def do_clean_local(number):
    """ Deletes local files
    """
    local("ls -t versions/web_static* | tail -n +{} | xargs rm -rf --"
          .format(number))


@task(default=True)
def do_clean(number=0):
    """ Deletes out-of-date archives
        usage: fab -f 100-clean_web_static.py do_clean
    """
    print("Cleaning local files")
    try:
        number = int(number)
        if number < 0:
            return False
    except Exception:
        return False

    number = (number, 1)[number <= 1] + 1
    do_clean_local(number)
    with cd("/data/web_static/releases/"):
        run("ls -td web_static* | tail -n +{} | xargs rm -rf --"
            .format(number))
    return True
