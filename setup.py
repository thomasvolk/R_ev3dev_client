#!/usr/bin/env python3

from setuptools import setup, Command, find_packages
import unittest


class RunClientCommand(Command):
    user_options = [
      # The format is (long option, short option, description).
      ('host=', 'H', 'rev3 host'),
      ('port=', 'p', 'rev3 port'),
    ]

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""
        self.host = 'ev3dev.local'
        self.port = '9999'

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        import sys
        sys.path.append('examples')
        from client_shell import REV3ClientShell
        print("open client host={} port={}".format(self.host, self.port))
        REV3ClientShell(
            host=self.host,
            port=int(self.port),
            buffer_size=2048).run()


def project_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='R_ev3dev_client',
      version="0.1",
      include_package_data=True,
      packages=find_packages(),
      test_suite="setup.project_test_suite",
      install_requires=[],
      python_requires='>3.4.0',
      cmdclass={'run_client': RunClientCommand})
