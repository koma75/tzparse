#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tzdata implementation"""

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
import openpyxl
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
    """Parse the Zone entry in the database.

    Args:
        lines (Array): Array containing the lines for a single Zone entry
        verbose (Int): verbosity mode

    Returns:
        Dict: zinfo data
    """
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

def parseLink(line, verbose):
    """Parse the Link entry in the database.

    Args:
        line (Str): line containing a single Link entry
        verbose (Int): verbosity mode

    Returns:
        Dict: zlink
    """
    line = re.split(r'[\t ]', line)
    pout("parseLink: {l}".format(l=line), verbose, Level.DEBUG)
    zlink = {
        line[2] : line[1]
    }
    return zlink

def parseRule(line, verbose):
    """Parse the Rule entry in the database.

    Args:
        line (Str): line containing a single Rule entry
        verbose (Int): verbosity mode

    Returns:
        Array: parsed rule data
    """
    pout("parseRule: {l}".format(l=line), verbose, Level.DEBUG)
    rule = line.split()
    return rule

def expandLink(linkSrc, linkDst, zinfos, verbose):
    """expand the link to a full zone info

    Args:
        linkSrc (Str): timezone name of source
        linkDst (Str): timezone name of link dest
        zinfos (Dict): timezone database structure to copy data from
        verbose (Int): verbosity mode

    Returns:
        Dict: zone information data
    """
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
    """Parse a single Timezone Database file.
    zinfos contains the parsed timezone information.
    rules contains the parsed rules.

    Args:
        fpath (Str): file path to the database file
        verbose (Int): verbosity mode

    Returns:
        Tuple: returns (zinfos, rules)
    """
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
    """Parse the list of timezone databases
    zinfos contains the parsed timezone information.
    rules contains the parsed rules.

    Args:
        tzdbs (Array): list of timezone database file paths
        tzdir (Str): directory the database file is located
        verbose (Int): verbosity mode

    Returns:
        Tuple: zinfos, rules
    """
    zinfos = {}
    rules = []
    for db in tzdbs:
        fpath = os.path.join(tzdir, db)
        retZInfo, retRules = parseTZDB(fpath, verbose)
        zinfos.update(retZInfo)
        rules.extend(retRules)

    return zinfos, rules

def createConf(conf, verbose):
    try:
        with click.open_file(conf, 'w', 'utf-8') as fd:
            fd.writelines([
                "zones: zone1970.tab\n",
                "countrylist: iso3166.tab\n",
                "tzdata:\n",
                "  - africa\n",
                "  - antarctica\n",
                "  - asia\n",
                "  - australasia\n",
                "  - europe\n",
                "  - northamerica\n",
                "  - southamerica\n",
                "output:\n",
                "  zonecsv: zones.csv\n",
                "  rulescsv: rules.csv\n",
                "  tzdataxls: tzdata.xlsx\n",
            ])
    except:
        pout("could not create {file}".format(file=conf), verbose, Level.ERROR)
    pass

def createWB(zlist, rules, verbose):
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.append(["Country","Zone","STDOFF","Rule","Coordinate","Comment"])
    ws.title = "Time Zones"
    for zone in zlist:
        for country in zlist[zone]["Countries"]:
            ws.append([
                country,
                zone,
                zlist[zone]["STDOFF"],
                zlist[zone]["Rule"],
                zlist[zone]["Coord"],
                zlist[zone]["Comment"]
            ])

    ws2 = wb.create_sheet("Rules", 1)
    ws2.append(["NAME","FROM","TO","TYPE","IN","ON","AT","SAVE","LETTER/S"])
    for rule in rules:
        #rule.pop(0)
        ws2.append(rule)
    return wb

def parse(kwargs):
    """Parse the tz database files and emmit CSV

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout("Command line arguments:", verbose, Level.INFO)
    pout(pformat(kwargs,depth=3,indent=4), verbose, Level.INFO)
    # 0. Get information from config.yml
    # If file does not exist, create a default config file
    if not os.path.exists(kwargs['config']):
        createConf(kwargs['config'], verbose)
    try:
        with click.open_file(kwargs['config'], 'r') as cnf:
            conf = yaml.safe_load(cnf)
    except:
        pout("could not open config file: {file}".format(file=kwargs['config']), verbose, Level.ERROR)

    if kwargs['zones']:
        conf['output']['zonecsv'] = kwargs['zones']
        pass
    if kwargs['rules']:
        conf['output']['rulescsv'] = kwargs['rules']
        pass
    if kwargs['xlsx']:
        conf['output']['tzdataxls'] = kwargs['xlsx']
        pass

    pout("Read config file:", verbose, Level.INFO)
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

    # 6. output results
    if kwargs["overwrite"]:
        fmode = 'w'
    else:
        fmode = 'x'

    # 6.1 Output Rules
    fpath = conf['output']['rulescsv']
    try:
        with click.open_file(fpath , mode=fmode, encoding="utf-8") as f:
            pout("writing {file}".format(file=fpath), verbose, Level.INFO)
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(["NAME","FROM","TO","TYPE","IN","ON","AT","SAVE","LETTER/S"])
            for rule in rules:
                rule.pop(0)
                writer.writerow(rule)
            pass
    except FileExistsError:
        pout("{file} already exists. use '-o' to overwrite".format(file=fpath), verbose, Level.ERROR)
    except:
        pout("Failed to write {file}".format(file=fpath), verbose, Level.ERROR)

    # 6.2 Output Time Zones
    fpath = conf['output']['zonecsv']
    try:
        with click.open_file(fpath, mode=fmode, encoding="utf-8") as f:
            pout("writing {file}".format(file=fpath), verbose, Level.INFO)
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
        pout("{file} already exists. use '-o' to overwrite".format(file=fpath), verbose, Level.ERROR)
    except:
        pout("Faild to write: {file}".format(file=fpath), verbose, Level.ERROR)

    # 6.3 Output Excel spreadsheet
    fpath = conf['output']['tzdataxls']
    if os.path.exists(fpath) and not kwargs['overwrite']:
        pout("{file} already exists. use '-o' to overwrite".format(file=fpath), verbose, Level.ERROR)
    else:
        pout("writing {file}".format(file=fpath), verbose, Level.INFO)
        wb = createWB(zlist, rules, verbose)
        wb.save(fpath)

    pass
