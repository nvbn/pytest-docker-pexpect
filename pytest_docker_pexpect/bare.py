import sys
import pexpect


def spawnu(source_root, tag, dockerfile, command):
    """Creates pexpect's spwanu attached to command.

    :type source_root: basestring
    :type tag: basestring
    :type dockerfile: basestring
    :type command: basestring
    :rtype: pexpect.spawnu

    """
    proc = pexpect.spawnu(command, logfile=sys.stderr)
    proc.docker_container_id = None
    proc.docker_inspect = lambda: {}
    return proc
