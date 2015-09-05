from functools import partial
import os
import six
import pytest
import pexpect
from . import docker, bare


def pytest_addoption(parser):
    """Adds `--run-without-docker` argument."""
    group = parser.getgroup("docker_pexpect")
    group.addoption('--run-without-docker', action="store_true", default=False,
                    help="Don't use docker")


@pytest.fixture
def run_without_docker(request):
    """Equals to `True` when containers not used."""
    return request.config.getoption('run_without_docker')


@pytest.fixture
def spawnu(run_without_docker):
    """Returns `spawnu` function depending on current mode."""
    spawnu_fn = bare.spawnu if run_without_docker else docker.spawnu
    cwd = os.getcwdu() if six.PY2 else os.getcwd()
    return partial(spawnu_fn, cwd)


@pytest.fixture(scope="function")
def TIMEOUT():
    return pexpect.TIMEOUT
