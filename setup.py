#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PyMata',
    packages=['PyMata'],
    version='2.03',
    description="A Python Protocol Abstraction Library For Arduino Firmata",
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    url='https://github.com/MrYsLab/PyMata',
    download_url = 'https://github.com/MrYsLab/PyMata',
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
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Home Automation',
    ],
)
