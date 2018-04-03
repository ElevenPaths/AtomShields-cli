# -*- coding: utf-8 -*-
u"""
Copyright 2018 ElevenPaths - Telefonica Digital España

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import shutil, os, stat
from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install as install_py
from setuptools.command.bdist_egg import bdist_egg
# from distutils.core import setup
from distutils.cmd import Command

def read_file(filename):
    with open(filename) as f:
        return f.read()


class AscliCommand(Command):
    description = 'Install ascli as binary into $PATH'
    user_options = []





    def initialize_options(self):
        """Set default values for options."""
        self.file = open("/tmp/ascli.log", "w")

    def finalize_options(self):
        """Post-process options."""
        pass

    def log(self, msg):
        if self.file is None:
            self.file = open("/tmp/ascli.log", "w")
        else:
            self.file.write(msg)
            self.file.write("\n")
        print msg

    def run(self):
        self.log("Instalando ascli. . . .")
        # Install as binary
        paths = ["/usr/local/bin", "/usr/bin", "/usr/sbin"]
        installed = False
        for path in paths:
            if os.access(path, os.W_OK):
                #Copy file
                source = os.path.join(os.path.dirname(__file__), package_name, 'cli.py')
                destination = os.path.join(path, "ascli")
                shutil.copy(source, destination)
                # Add a+x
                st = os.stat(destination)
                os.chmod(destination, st.st_mode | stat.S_IEXEC)
                self.log("{package} installed into {destination}".format(package=package_name, destination=destination))
                installed = True
                break

        if not installed:
            from termcolor import colored
            self.log(colored("[!] CLI not installed in PATH. PLease try again with root permissions", "red"))


class BuildPyCommand(build_py):
    """Custom build command."""

    def run(self):
        build_py.run(self)
        self.run_command('ascli')


class InstallCommand(install_py):
    """Custom install command."""

    def run(self):
        install_py.run(self)
        self.run_command('ascli')

class BdistCommand(bdist_egg):
    def run(self):
        install_py.run(self)
        self.run_command('ascli')

package_name = 'atomshieldscli'
version = read_file('VERSION').strip()

setup(
  name = package_name,
  version = version,
  install_requires=read_file('requirements.txt').splitlines(),
  packages = find_packages(),
  author = 'ElevenPaths',
  description = "Command-Line Interface for atomshields package.",
  long_description=open('README.rst').read(),
  author_email = 'diego.fernandez@11paths.com, david.amrani@11paths.com',
  url = 'https://github.com/ElevenPaths/AtomShields-cli',
  project_urls={
      "Documentation": "https://atomshields.readthedocs.io",
      "Source Code": "https://github.com/ElevenPaths/AtomShields-cli",
  },
  download_url = 'https://github.com/ElevenPaths/AtomShields-cli/tarball/' + version,
  keywords = 'security, source code, analysis',
  license='Apache 2.0',
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Intended Audience :: Other Audience',
      'License :: OSI Approved :: Apache Software License',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.7',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Software Development :: Quality Assurance',
      'Topic :: Software Development :: Testing',
  ],
  cmdclass = {
    'ascli': AscliCommand,
    'install': InstallCommand,
    'build_py': BuildPyCommand,
    'bdist_egg': BdistCommand
  }
)
