import pytest


@pytest.mark.containers(
    (u'pytest-docker-pexpect/ubuntu-bash',
     u'''FROM ubuntu:latest
         RUN apt-get update
         RUN apt-get install -yy bash''',
     u'bash'),
    (u'pytest-docker-pexpect/ubuntu-zsh',
     u'''FROM ubuntu:latest
         RUN apt-get update
         RUN apt-get install -yy zsh''',
     u'zsh'))
def test_echo(container, TIMEOUT):
    """Ensures that all works.

    :type container: pexpect.spawnu

    """
    container.sendline(u'echo 1')
    assert container.expect([TIMEOUT, u'1'])
