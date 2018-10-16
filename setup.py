from setuptools import setup, find_packages

version = '0.6'

setup(name='pytest-docker-pexpect',
      version=version,
      description="pytest plugin for writing functional tests with pexpect and docker",
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/pytest-docker-pexpect',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['pexpect', 'pytest', 'six'],
      entry_points={'pytest11': [
          'docker_pexpect = pytest_docker_pexpect.plugin']})
