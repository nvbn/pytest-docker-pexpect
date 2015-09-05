import sys
import subprocess
import shutil
from tempfile import mkdtemp
import os
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
    return spawned
