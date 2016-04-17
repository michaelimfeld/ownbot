# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from setuptools import setup


setup(
    name="ownbot",
    version="0.0.1",
    license="MIT",
    description="Python module to create private telegram bots.",
    author="Michael Imfeld",
    author_email="michaelimfeld@crooked.ch",
    maintainer="Michael Imfeld",
    maintainer_email="michaelimfeld@crooked.ch",
    platforms=["Linux", "Windows", "MAC OS X"],
    url="https://github.com/michaelimfeld/ownbot",
    download_url="https://github.com/michaelimfeld/ownbot",
    packages=["ownbot"],
    package_data={"": ["*.md"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing"
    ],
)
