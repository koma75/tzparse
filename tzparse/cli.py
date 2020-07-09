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
from tzparse.tzdata import tzdata
# Import the version information
from tzparse.version import __version__

@click.command()
@click.option(
    '--config', '-c', default="./config.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: config.yml)'
    )
@click.argument(
    'tzdir',
    type=click.Path(exists=True, file_okay=False, readable=True, resolve_path=True),
)
@click.option(
    '--zones', '-z',
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<zones>',
    help='zone csv output file'
    )
@click.option(
    '--rules', '-r',
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<rules>',
    help='rule csv output file'
    )
@click.option(
    '--xlsx', '-x',
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<tzxl>',
    help='timezone data xlsx output file'
    )
@click.option(
    '--overwrite', '-o', is_flag=True,
    help='overwrite output files (default: False)'
)
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
@click.version_option(version=__version__)
def cli(**kwargs):
    """IANA timezone database parser.
    Parse data available at https://www.iana.org/time-zones

    Download tzdataXXXX.tar.gz file and extract contents to parse.

    Config file must be provided to define input files.
    See example config.yml below:

    \b
        zones: zone1970.tab
        countrylist: iso3166.tab
        tzdata:
            - africa
            - antarctica
            - asia
            - australasia
            - europe
            - northamerica
            - southamerica
        output:
            zonecsv: zones.csv
            rulescsv: rules.csv
            tzdataxls: tzdata.xlsx

    Command line options takes precedance over the command line option
    """
    tzdata.parse(kwargs)

# Entry point
def main():
    """Main script."""
    cli()

if __name__ == '__main__':
    main()
