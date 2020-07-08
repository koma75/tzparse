#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""exif sort implementation"""

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

from enum import IntEnum

import yaml
import csv
import os
import re
from pprint import pformat
import click

class Level(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

def pout(msg=None, Verbose=0, level=Level.INFO, newline=True):
    """stdout support method

    Keyword Arguments:
        msg {string} -- message to print (default: {None})
        Verbose {Int} -- Set True to print DEBUG message (default: {0})
        level {Level} -- Set message level for coloring (default: {Level.INFO})
        newline {bool} -- set to False if trailing new line is not needed (default: {True})
    """
    error=False
    if level in {Level.NOTSET, Level.DEBUG}:
        # blah
        if Verbose < 2:
            return
        fg = 'magenta'
    elif level == Level.INFO:
        fg = 'green'
    elif level == Level.WARNING:
        if Verbose < 1:
            return
        fg = 'yellow'
        error=True
    elif level in {Level.ERROR, Level.CRITICAL}:
        fg = 'red'
        error=True
    else:
        pass
    click.echo(click.style(str(msg), fg=fg), nl=newline, err=error)

"""
input data sample reference
kwargs sample
{   'config': <_io.TextIOWrapper name='config.yml' mode='r' encoding='UTF-8'>,
    'overwrite': False,
    'rules': '/path/to/working/dir/rules.csv',
    'tzdir': '/path/to/workinng/dir/tzdb-2020a',
    'verbose': 2,
    'zones': '/path/to/working/dir/zones.csv'}
config file sample
{   'countrylist': 'iso3166.tab',
    'tzdata': [   'africa',
                  'antarctica',
                  'asia',
                  'australasia',
                  'europe',
                  'northamerica',
                  'southamerica'],
    'zones': 'zone1970.tab'}
"""

def getCountry(isoFile, tzdir, verbose):
    """Get the dictionary containing the iso3166 country code to name conversion

    Args:
        isoFile (string): file name of the iso3166.tab file
        tzdir (string): path holding the zoneFile
        verbose (string): verbosity level

    Returns:
        dict: dictionary containing the conversion from iso3166 country code to country name
    """
    fpath = os.path.join(tzdir, isoFile)
    pout("processing {path}".format(path=fpath), verbose, Level.DEBUG)
    with open(fpath, encoding="utf-8") as fp:
        rdr = csv.reader(filter(lambda row: row[0]!='#', fp), delimiter='\t')
        countryList = {}
        for row in rdr:
            countryList[row[0]] = row[1]
    return countryList

def getZones(zoneFile, tzdir, clist, verbose):
    """Get the list of time zones from zone1970 tab file.

    Args:
        zoneFile (string): filename of the zone1970.tab file to use
        tzdir (string): path holding the zoneFile
        clist (dict): dictionary to convert iso3166 code to country name
        verbose (int): verbosity level

    Returns:
        dict: dictionary containing the zone list and their attributes
    """
    fpath = os.path.join(tzdir, zoneFile)
    pout("processing {path}".format(path=fpath), verbose, Level.DEBUG)
    with open(fpath, encoding="utf-8") as fp:
        rdr = csv.reader(filter(lambda row: row[0]!='#', fp), delimiter='\t')
        zoneList = {}
        for row in rdr:
            cnlist = []
            for ccode in row[0].split(','):
                if ccode in clist:
                    cnlist.append(clist[ccode])
                else:
                    cnlist.append("undefined")
            if len(row) > 3: # comment available
                zoneList[row[2]] = {"Countries":cnlist, "Coord": row[1], "Comment": row[3]}
            else:
                zoneList[row[2]] = {"Countries":cnlist, "Coord": row[1], "Comment": ''}

    return zoneList

def parseZone(lines, verbose):
    pout("parseZone: {l}".format(l = lines), verbose, Level.DEBUG)
    #pout(lines, verbose, Level.DEBUG)
    firstLine = lines.pop(0)
    firstLine = re.split(r'[\t ]', firstLine)
    pout(firstLine, verbose, Level.DEBUG)
    zinfo = {
        firstLine[1] : {
            "STDOFF" : firstLine[2],
            "Rule" : firstLine[3]
        }
    }
    if len(lines) > 0:
        lastLine = re.split(r'[\t ]', lines[(len(lines)-1)].lstrip())
        zinfo[firstLine[1]]["STDOFF"] = lastLine[0]
        zinfo[firstLine[1]]["Rule"] = lastLine[1]
    else:
        pout("{zone} does not have extra lines".format(zone = firstLine[1]), verbose, Level.WARNING)
    pout(zinfo, verbose, Level.DEBUG)
    return zinfo

#Link LNKTGT LNKSRC
#Link Asia/Bangkok Asia/Phnom_Penh	# Cambodia
#Link Asia/Bangkok Asia/Vientiane	# Laos

def parseLink(line, verbose):
    line = re.split(r'[\t ]', line)
    pout("parseLink: {l}".format(l=line), verbose, Level.DEBUG)
    zlink = {
        line[2] : line[1]
    }
    return zlink

def parseRule(line, verbose):
    pout("parseRule: {l}".format(l=line), verbose, Level.DEBUG)
    rule = line.split()
    return rule

def expandLink(linkSrc, linkDst, zinfos, verbose):
    pout("expanding: {src} -> {dst}".format(src=linkSrc, dst=linkDst), verbose, Level.DEBUG)
    zinfo = {
        linkSrc: {
            "STDOFF" : zinfos[linkDst]["STDOFF"],
            "Rule" : zinfos[linkDst]["Rule"],
        }
    }
    pout(pformat(zinfo,depth=3,indent=4), verbose, Level.DEBUG)
    return zinfo

def parseTZDB(fpath, verbose):
    zinfos = {}
    zlinks = {}
    rules = []
    pout("parseTZDB: {path}".format(path=fpath), verbose, Level.INFO)
    with click.open_file(fpath, 'r', encoding="utf-8") as db:
        line = db.readline()
        while line:
            # Strip comments and trailing spaces
            line = re.sub(r'^(.*)#.*', '\\1', line).rstrip()
            if re.match(r'Zone.*',line):
                lines = [line]
                line = db.readline()
                # Zones span multiple lines denoted by leading tabs
                while re.match(r'[\t\#]',line):
                    if re.match(r'\t',line):
                        # Strip comments and trailing spaces
                        line = re.sub(r'^(.*)#.*', '\\1', line).rstrip()
                        lines.extend([line])
                    line = db.readline()
                zinfos.update(parseZone(lines, verbose))
            elif re.match(r'Link.*',line):
                zlinks.update(parseLink(line, verbose))
                line = db.readline()
            elif re.match(r'Rule.*',line):
                rules.extend([parseRule(line, verbose)])
                line = db.readline()
            else:
                line = db.readline()
        pass
    # Some Links source different database files.
    pout("linking:\n{l}".format(l=zlinks), verbose, Level.DEBUG)
    for lnk in zlinks:
        zinfos.update(expandLink(lnk, zlinks[lnk], zinfos, verbose))
    return zinfos, rules

def parseTZDBs(tzdbs, tzdir, verbose):
    zinfos = {}
    rules = []
    for db in tzdbs:
        fpath = os.path.join(tzdir, db)
        retZInfo, retRules = parseTZDB(fpath, verbose)
        zinfos.update(retZInfo)
        rules.extend(retRules)

    return zinfos, rules

def parse(kwargs):
    """Parse the tz database files and emmit CSV

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout(pformat(kwargs,depth=3,indent=4), verbose, Level.DEBUG)
    # 0. Get information from config.yml
    conf = yaml.safe_load(kwargs['config'])
    pout(pformat(conf,depth=3,indent=4), verbose, Level.INFO)

    # 1. Parse iso3166.tab file
    #     * Hold the translation data in a Key-Value data.
    pout("Processing contry list: {clist}".format(clist=conf['countrylist']), verbose, Level.INFO)
    clist = getCountry(conf['countrylist'], kwargs['tzdir'], verbose)
    #pout(pformat(clist, depth=2,indent=4), verbose, Level.DEBUG)

    # 2. Parse all zone list file for all Zones
    #     * Hold the Zone information data with Key=Zone name and Value containing all other Zone definition.
    # 3. Parse all zone list file for all Links
    #     * Copy the Zone information of the linked zone to the defined zone.
    # 4. Parse all zone list file for all Rules
    #     * Can be parsed along with Zones and links
    zinfos, rules = parseTZDBs(conf['tzdata'], kwargs['tzdir'], verbose)
    pout("-------Final Zone Info List--------", verbose, Level.DEBUG)
    pout(pformat(zinfos, depth=4, indent=4), verbose, Level.DEBUG)
    pout("-------Final Rule List--------", verbose, Level.DEBUG)
    pout(pformat(rules, depth=2, indent=4,width=100), verbose, Level.DEBUG)

    # 5. Parse Zone.tab and construct the zones.csv file
    pout("Processing zone list: {clist}".format(clist=conf['zones']), verbose, Level.INFO)
    zlist = getZones(conf['zones'], kwargs['tzdir'], clist, verbose)
    for zone in zlist:
        zlist[zone]["Rule"] = zinfos[zone]["Rule"]
        zlist[zone]["STDOFF"] = zinfos[zone]["STDOFF"]
    pout("-------Final Zone DB--------", verbose, Level.DEBUG)
    pout(pformat(zlist, depth=3,indent=4), verbose, Level.DEBUG)

    # 6. output result to csv files
    if kwargs["overwrite"]:
        fmode = 'w'
    else:
        fmode = 'x'

    # 6.1 Output Rules
    try:
        with click.open_file(kwargs['rules'], mode=fmode, encoding="utf-8") as f:
            pout("writing {file}".format(file=kwargs['rules']), verbose, Level.INFO)
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(["NAME","FROM","TO","TYPE","IN","ON","AT","SAVE","LETTER/S"])
            for rule in rules:
                rule.pop(0)
                writer.writerow(rule)
            pass
    except FileExistsError:
        pout("{file} already exists. use '-o' to overwrite".format(file=kwargs['rules']), verbose, Level.ERROR)
    except:
        pout("Failed to write {file}".format(file=kwargs['rules']), verbose, Level.ERROR)

    # 6.2 Output Time Zones
    try:
        with click.open_file(kwargs['zones'], mode=fmode, encoding="utf-8") as f:
            pout("writing {file}".format(file=kwargs['zones']), verbose, Level.INFO)
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(["Country","Zone","STDOFF","Rule","Coordinate","Comment"])
            for zone in zlist:
                for country in zlist[zone]["Countries"]:
                    writer.writerow([
                        country,
                        zone,
                        zlist[zone]["STDOFF"],
                        zlist[zone]["Rule"],
                        zlist[zone]["Coord"],
                        zlist[zone]["Comment"]
                    ])
            pass
    except FileExistsError:
        pout("{file} already exists. use '-o' to overwrite".format(file=kwargs['zones']), verbose, Level.ERROR)
    #except:
    #    pout("Faild to write: {file}".format(file=kwargs['zones']), verbose, Level.ERROR)

    # Rule	NAME	FROM	TO	TYPE	IN	ON	AT	SAVE	LETTER/S
    # Rule	Syria	1920	1923	-	Apr	Sun>=15	2:00	1:00	S

    pass
