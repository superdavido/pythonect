#!/usr/bin/env python
# Copyright (c) 2012-2013, Itzik Kotler
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

try:

    import setuptools

except ImportError:

    from distribute_setup import use_setuptools

    use_setuptools()

    import setuptools


import sys
import distutils.core
import distutils.command.build
import subprocess
import re


# Functions

def _mk_versiondotpy():

    with open('pythonect/_version.py', 'wt') as f:

        f.write('# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN.\n__version__ = \'' + _safe_get_version() + '\'\n')


def __get_git_version():

    version = "0.0.0.dev0"

    try:

        git = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        git.stderr.close()

        git_output = git.stdout.readlines()[0]

        git_ver = re.match('^\w+(?P<MAJOR>\d+)\.(?P<MINOR>\d+)(\.(?P<MICRO>\d+)(\-(?P<DEV>\d+))?)?', git_output)

        if git_ver is not None:

            # MAJOR.MINOR

            version = git_ver.group('MAJOR') + '.' + git_ver.group('MINOR')

            if git_ver.groupdict('MICRO') is not None:

                # MAJOR.MINOR.MICRO

                version = version + '.' + git_ver.group('MICRO')

                if git_ver.groupdict('DEV') is not None:

                    # MAJOR.MINOR.MICRO-DEV

                    version = version + '.dev' + git_ver.group('DEV')

    except Exception as e:

        pass

    return version


def _safe_get_version():

    version = '0.0.0dev0'

    try:

        tmp_globals = {}

        # Tarball?

        execfile('pythonect/_version.py', tmp_globals)

        version = tmp_globals['__version__']

    except Exception:

        # Git repository?

        version = __get_git_version()

    return version


# Classes

class Version(distutils.core.Command):

    description = ""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        # Generate `_version.py`

        _mk_versiondotpy()

        print "*** Pythonect Version %s ***" % (_safe_get_version())


# Entry Point

if __name__ == "__main__":

    dependencies = ['networkx>=1.7', 'nose']

    major, minor = sys.version_info[:2]

    python_27 = (major > 2 or (major == 2 and minor >= 7))

    # < Python 2.7 ?

    if not python_27:

        # Python 2.6

        dependencies = dependencies + ['argparse', 'importlib', 'unittest2']

    setupconf = dict(
        name='Pythonect',
        version=_safe_get_version(),
        author='Itzik Kotler',
        author_email='xorninja@gmail.com',
        url='http://www.pythonect.org/',
        license='BSD',
        description='A general-purpose dataflow programming language based on Python, written in Python',

        long_description=open('README.rst').read(),
        scripts=['bin/pythonect'],
        data_files=[('', ['LICENSE'])],
        packages=setuptools.find_packages(),

        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 2.6',
        ],

        install_requires=dependencies,

        cmdclass={'version': Version},

        test_suite='nose.collector',

        zip_safe=False
    )

    setuptools.setup(**setupconf)
