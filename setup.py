#!/usr/bin/env python
try:
    from setuptools import setup
    extra = dict(include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

def get_version():
    from os.path import abspath, dirname, join
    basedir = abspath(dirname(__file__))
    from imp import load_source
    version = load_source('version', join(basedir, 'dreampylib', 'version.py'))
    return version.VERSION

def main():
    setup(
        name            = 'dreampylib',
        version         = get_version(),
        description     = "A python library for interacting with Dreamhost's API",
        long_description    = open("README.md").read(),
        author              = "Eli Ribble",
        author_email        = "junk@theribbles.org",
        install_requireds   = [],
        packages            = ['dreampylib'],
        package_data        = {'dreampylib': ['dreampylib/*']},
        scripts             = [],
        **extra
    )

if __name__ == '__main__':
    main()
