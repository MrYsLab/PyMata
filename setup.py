#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PyMata',
    packages=['PyMata'],
    version='1.3',
    description="A Python Protocol Abstraction Library For Arduino Firmata",
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    install_requires=['pyserial'],
    url='https://github.com/MrYsLab/PyMata',
    download_url = ' https://github.com/MrYsLab/PyMata/tarball/1.3',
    keywords = ['Firmata', 'Arduino', 'Protocol'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Home Automation',
    ],
)
