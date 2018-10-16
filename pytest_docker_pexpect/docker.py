import sys
import subprocess
import shutil
from tempfile import mkdtemp
import os
import json
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


def get_container_id(tag, command):
    """Returns container id for spawned pexpect.
    
    :type tag: basestring
    :rtype: basestring
    
    """
    proc = subprocess.Popen(
        ['docker', 'ps', '--format', '{{json .}}'],
        stdout=subprocess.PIPE)

    for line in proc.stdout.readlines():
        data = json.loads(line.decode())
        if tag in data['Image'] and command in data['Command']:
            return data['ID']


def inspect(container_id):
    proc = subprocess.Popen(
        ['docker', 'inspect', '--format', '{{json .}}', container_id],
        stdout=subprocess.PIPE)
    data = proc.stdout.read().decode()
    return json.loads(data)


def stats(container_id):
    proc = subprocess.Popen(
        ['docker', 'stats', '--no-stream',
         '--format', '{{json .}}', container_id],
        stdout=subprocess.PIPE)
    data = proc.stdout.read().decode()
    return json.loads(data)


def spawnu(source_root, tag, dockerfile, command):
    """Creates pexpect spawnu attached to docker.

    :type source_root: basestring
    :type tag: basestring
    :type dockerfile: basestring
    :type command: basestring
    :rtype: pexpect.spawnu

    """
    build_container(tag, dockerfile)
    spawned = pexpect.spawnu(
        'docker', ['run', '--rm=true', '--volume',
                   '{}:/src'.format(source_root),
                   '--tty=true', '--interactive=true',
                   tag, command],
        logfile=sys.stderr)

    spawned.docker_container_id = get_container_id(tag, command)
    spawned.docker_inspect = lambda: inspect(spawned.docker_container_id)
    spawned.docker_stats = lambda: stats(spawned.docker_container_id)

    return spawned
