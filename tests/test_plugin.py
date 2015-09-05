import pytest


@pytest.fixture(
    params=((u'pytest-docker-pexpect/ubuntu-bash',
             u'''FROM ubuntu:latest
                 RUN apt-get update
                 RUN apt-get install -yy bash''',
             u'bash'),
            (u'pytest-docker-pexpect/ubuntu-zsh',
             u'''FROM ubuntu:latest
                 RUN apt-get update
                 RUN apt-get install -yy zsh''',
             u'zsh')))
def proc(request, spawnu):
    return spawnu(*request.param)


@pytest.mark.once_without_docker
def test_echo(proc, TIMEOUT):
    """Ensures that all works.

    :type proc: pexpect.spawnu

    """
    proc.sendline(u'echo 1')
    assert proc.expect([TIMEOUT, u'1'])
