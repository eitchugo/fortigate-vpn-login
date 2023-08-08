# -*- coding: utf-8 -*-
"""
    fortigate-vpn-login setup script
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Setup script for packaging and installing fortigate-vpn-login
"""
import pathlib
from setuptools import setup, find_packages

this_directory = pathlib.Path(__file__).parent.resolve()
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

setup(
    name='fortigate-vpn-login',
    version='0.5',
    description='Uses openconnect to connect to Fortinet VPNs, with extra features',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hugo Cisneiros',
    author_email='hugo.cisneiros@gmail.com',
    url='https://github.com/eitchugo/fortigate-vpn-login',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: System :: Networking'
    ],
    keywords='vpn, security, openconnect, fortinet',
    packages=find_packages(include=['fortigate_vpn_login']),
    python_requires=">=3.8, <4",
    install_requires=[
        'requests==2.31.0',
        'xmltodict==0.13.0',
        'beautifulsoup4==4.12.2',
        'werkzeug==2.3.6',
        'markupsafe==2.1.3',
        'psutil==5.9.5'
    ],
    entry_points={
        'console_scripts': [
            'fortigate-vpn-login=fortigate_vpn_login.cli:main'
        ]
    }
)
