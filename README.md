# pytest-docker-pexpect

py.test plugin for writing simple functional tests with pexpect and docker.

## Installation

```python
pip install pytest-docker-pexpect
```

## Usage

The plugin provides `pytest.mark.containers(*container_tuples)` marker
that accepts container tuples in format `(container_tag, dockerfile, command)`.
It automatically passed `pexpect.spawnu` object to a test function
as a `container` parameter:

```python
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
    container.sendline(u'echo 1')
    assert container.expect([TIMEOUT, u'1'])
```

Also the plugin provides `TIMEOUT` fixture, that can be used for simple asserts, like:

```python
assert container.expect([TIMEOUT, u'1'])
```

## Usage without docker

With flag `--run-without-docker` tests can be run in environment without docker (e.g. travis-ci).
In this mode tests runs only for first container and docker initialization steps are skipped.
Be careful, in this mode all commands will be execute directly on local system!

## Licensed under MIT
