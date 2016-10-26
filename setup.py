# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from setuptools import setup

setup(
    name="ownbot",
    version="0.0.4",
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
    install_requires=[
        "python-telegram-bot",
        "PyYAML"
    ],
    include_package_data=True,
    keywords=[
        "ownbot", "python",
        "telegram", "bot"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
    ]
)
