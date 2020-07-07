#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main CLI Setup and Entrypoint."""

# BSD 2-Clause License
#
# Copyright (c) 2019, Yasuhiro Okuno (Koma)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, division, print_function

# Import the main click library
import click
# Import the sub-command implementations
from tzparse.subcmd import subcmd
# Import the version information
from tzparse.version import __version__

@click.command()
@click.option(
    '--config', '-c', default="config.yml", type=str,
    metavar='<cfg>',
    help='Configuration File (default: config.yml)'
    )
@click.option(
    '--tzdata', '-t', default="./tzdata/", type=str,
    metavar='<tzdata>',
    help='input tzdata folder (default: tzdata)'
    )
@click.option(
    '--zones', '-z', default="./zones.csv", type=str,
    metavar='<zones>',
    help='zone csv output file (default: zones.csv)'
    )
@click.option(
    '--rules', '-r', default="./rules.csv", type=str,
    metavar='<rules>',
    help='rule csv output file (default: rules.csv)'
    )
@click.option(
    '--verbose', '-v', is_flag=True,
    help='output in verbose mode'
    )
@click.version_option(version=__version__)
def cli(**kwargs):
    """IANA timezone database parser."""
    subcmd.subcmd1(kwargs)

# Entry point
def main():
    """Main script."""
    cli()

if __name__ == '__main__':
    main()
