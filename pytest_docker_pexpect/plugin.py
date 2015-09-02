import os
import pytest
import pexpect
from . import docker, bare


def pytest_addoption(parser):
    """Adds `--run-without-docker` argument."""
    group = parser.getgroup("docker_pexpect")
    group.addoption('--run-without-docker', action="store_true", default=False,
                    help="Don't use docker")


def pytest_configure(config):
    """Adds `containers` marker."""
    config.addinivalue_line(
        "markers", "containers(container, ...): pass container pexpects' spawnu"
                   "with ran docker container.")


def spawnu(is_bare, tag, dockerfile, command):
    """Returns `spawnu` depending on current mode.

    :type is_bare: bool
    :type tag: basestring
    :type dockerfile: basestring
    :type command: basestring

    """
    spawnu_fn = bare.spawnu if is_bare else docker.spawnu
    return spawnu_fn(os.getcwd(), tag, dockerfile, command)


def pytest_generate_tests(metafunc):
    marker = getattr(metafunc.function, 'containers', None)
    if marker:
        is_bare = metafunc.config.getoption('run_without_docker')
        if is_bare:
            containers = [marker.args[0]]
        else:
            containers = marker.args
        containers = (spawnu(is_bare, *container) for container in containers)
        metafunc.parametrize('container', containers)


@pytest.fixture(scope="function")
def TIMEOUT():
    return pexpect.TIMEOUT
