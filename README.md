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

`spawnu` provides [pexpect API](https://pexpect.readthedocs.io/en/stable/api/pexpect.html#spawn-class)
and additional docker-specific API:

* `proc.docker_container_id` &ndash; container id
* `proc.docker_inspect()` &ndash; decoded json output of `docker inspect`
* `proc.docker_stats()` &ndash; decoded json output of `docker stats`


Also the plugin provides `TIMEOUT` fixture, that can be used for simple asserts, like:

```python
assert proc.expect([TIMEOUT, u'1'])
```

`run_without_docker` fixtures, that indicates that docker isn't used.

If you want to disable tests if docker isn't available, use `@pytest.mark.skip_without_docker`.

If you want to run parametrized test only once without docker, use
`@pytest.mark.once_without_docker`.

## Usage without docker

With flag `--run-without-docker` tests can be run in environment without docker (e.g. travis-ci).
In this mode tests runs only for first container and docker initialization steps are skipped.
Be careful, in this mode all commands will be execute directly on local system!

## Licensed under MIT
