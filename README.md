# pytest-docker-pexpect [![Build Status](https://travis-ci.org/nvbn/pytest-docker-pexpect.svg?branch=master)](https://travis-ci.org/nvbn/pytest-docker-pexpect)

py.test plugin for writing simple functional tests with pexpect and docker.

## Installation

```python
pip install pytest-docker-pexpect
```

## Usage

The plugin provides `spawnu` fixture, that could be called like
`spawnu(tag, dockerfile, command)`, it returns `pexpect.spwanu` attached to `command`
runned inside a container that built with `tag` and `dockerfile`:

```python
def test_echo(spawnu):
    proc = spawnu(u'ubuntu', u'FROM ubuntu:latest', 'bash')
    proc.sendline(u'ls')
```

Also the plugin provides `TIMEOUT` fixture, that can be used for simple asserts, like:

```python
assert proc.expect([TIMEOUT, u'1'])
```

And `run_without_docker` fixtures, that indicates that docker isn't used.

## Usage without docker

With flag `--run-without-docker` tests can be run in environment without docker (e.g. travis-ci).
In this mode tests runs only for first container and docker initialization steps are skipped.
Be careful, in this mode all commands will be execute directly on local system!

## Licensed under MIT
