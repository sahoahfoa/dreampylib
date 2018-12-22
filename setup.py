#!/usr/bin/env python3
"""DreamlibPy setup and install"""
try:
    from setuptools import setup, find_packages

    EXTRA = dict(include_package_data=True)
except ImportError:
    from distutils.core import setup

    EXTRA = {}


def get_version():
    """Retrive version"""
    from os.path import abspath, dirname, join

    basedir = abspath(dirname(__file__))
    from imp import load_source

    version = load_source("version", join(basedir, "dreampylib", "version.py"))
    return version.VERSION


def main():
    """Run installer"""
    setup(
        name="dreampylib",
        version=get_version(),
        description="A python library for interacting with Dreamhost's API",
        long_description=open("README.md").read(),
        author="Eli Ribble",
        author_email="junk@theribbles.org",
        install_requires=["dnspython", "requests"],
        packages=find_packages(),
        package_data={"dreampylib": ["dreampylib/*"]},
        entry_points={
            'console_scripts': [
                'dh_list_commands = dreampylib.tools.dh_list_commands:main',
                'dh_update_dns = dreampylib.tools.dh_update_dns:main',
                'dh_run = dreampylib.tools.dh_run:main',
            ]
        },
        **EXTRA
    )


if __name__ == "__main__":
    main()
