import sys
import subprocess
import shutil
from tempfile import mkdtemp
import os
import json
import atexit
import pexpect


def build_container(tag, dockerfile):
    """Builds docker container.

    :type tag: basestring
    :type dockerfile: basestring
    :type source_root: basestring

    """
    tmpdir = mkdtemp()
    try:
        dockerfile_path = os.path.join(tmpdir, 'Dockerfile')
        with open(dockerfile_path, 'w') as file:
            file.write(dockerfile)
        if subprocess.call(['docker', 'build', '--tag={}'.format(tag), tmpdir]) != 0:
            raise Exception("Can't build a container")
    finally:
        shutil.rmtree(tmpdir)



def inspect(container_id):
    """Returns output of `docker --inspect`

    :type container_id: basestring
    :rtype: dict

    """
    proc = subprocess.Popen(
        ['docker', 'inspect', '--format', '{{json .}}', container_id],
        stdout=subprocess.PIPE)
    data = proc.stdout.read().decode()
    return json.loads(data)


def stats(container_id):
    """Returns output of `docker --stats`

    :type container_id: basestring
    :rtype: dict

    """
    proc = subprocess.Popen(
        ['docker', 'stats', '--no-stream',
         '--format', '{{json .}}', container_id],
        stdout=subprocess.PIPE)
    data = proc.stdout.read().decode()
    return json.loads(data)


def run(source_root, tag, command, docker_run_arguments):
    """Runs docker container in detached mode.

    :type source_root: basestring
    :type tag: basestring
    :type command: basestring
    :rtype: basestring

    """
    proc = subprocess.Popen(
        ['docker', 'run', '--rm=true', '--volume',
         '{}:/src'.format(source_root),
         '--tty=true', '--interactive=true',
         '--detach'] + docker_run_arguments + [tag, command],
        stdout=subprocess.PIPE)
    return proc.stdout.readline().decode()[:-1]


def kill(container_id):
    """Kills docker container.

    :type container_id: basestring

    """
    subprocess.call(['docker', 'kill', container_id],
                    stdout=subprocess.PIPE)


def spawnu(source_root, tag, dockerfile, command, docker_run_arguments=None):
    """Creates pexpect spawnu attached to docker.

    :type source_root: basestring
    :type tag: basestring
    :type dockerfile: basestring
    :type command: basestring
    :type docker_run_arguments: list
    :rtype: pexpect.spawnu

    """
    if docker_run_arguments is None:
        docker_run_arguments = []

    build_container(tag, dockerfile)
    container_id = run(source_root, tag, command, docker_run_arguments)
    atexit.register(kill, container_id)

    spawned = pexpect.spawnu('docker', ['attach', container_id],
                             logfile=sys.stderr)

    spawned.docker_container_id = container_id
    spawned.docker_inspect = lambda: inspect(container_id)
    spawned.docker_stats = lambda: stats(container_id)

    return spawned
