tzparse
========================================================================

Command line tool to parse [IANA tzdata][IANA]
for the latest time zone information.

This tool is intended as an aid for users, to help them select timezones
appropriate for their practical needs.  It is not intended to take or
endorse any position on legal or territorial claims, as also stated by
the database.

Installation
------------------------------------------------------------------------

~~~shell
> pip install git+https://github.com/koma75/tzparse
~~~

Usage
------------------------------------------------------------------------

### Preparation

First, download the latest [IANA tzdata][IANA] from the link and extract
the contents to some directory.

### Executing the command

~~~shell
Usage: tzparse [OPTIONS] TZDIR

  IANA timezone database parser. Parse data available at
  https://www.iana.org/time-zones

  Download tzdataXXXX.tar.gz file and extract contents to parse.

  Config file must be provided to define input files. See example config.yml
  below:

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

Options:
  -c, --config <cfg>   Configuration File (default: config.yml)
  -z, --zones <zones>  zone csv output file
  -r, --rules <rules>  rule csv output file
  -x, --xlsx <tzxl>    timezone data xlsx output file
  -o, --overwrite      overwrite output files (default: False)
  -v, --verbose        output in verbose mode
  --version            Show the version and exit.
  --help               Show this message and exit.
~~~

Prepare a config file that specify which files to read from
the tzdata folder (example below), and specify the file using --config
option.

~~~yaml
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
  ~~~

Execute the command by specifying the directory which you downloaded
earlier.
TZDIR argument and the --config option is mandatory.
Other options may be specified to change certain operations.

Building an Executable
------------------------------------------------------------------------

Install pyinstaller and package the project.
May want to use venv when executing the pyinstaller.



First, enter venv and install the local package and pyinstaller

~~~shell
>. .venv/Scripts/activate
(.venv) D:\work\tzparse>pip install .
Processing d:\work\tzparse
Requirement already satisfied: click<8,>=7 in d:\work\tzparse\.venv\lib\site-packages (from tzparse==0.2.0) (7.1.2)
Requirement already satisfied: colorama<0.5,>=0.4 in d:\work\tzparse\.venv\lib\site-packages (from tzparse==0.2.0) (0.4.3)
Requirement already satisfied: pyyaml<6,>=5 in d:\work\tzparse\.venv\lib\site-packages (from tzparse==0.2.0) (5.3.1)
Requirement already satisfied: openpyxl<4,>=3 in d:\work\tzparse\.venv\lib\site-packages (from tzparse==0.2.0) (3.0.4)
Requirement already satisfied: et-xmlfile in d:\work\tzparse\.venv\lib\site-packages (from openpyxl<4,>=3->tzparse==0.2.0) (1.0.1)
Requirement already satisfied: jdcal in d:\work\tzparse\.venv\lib\site-packages (from openpyxl<4,>=3->tzparse==0.2.0) (1.4.1)
Using legacy setup.py install for tzparse, since package 'wheel' is not installed.
Installing collected packages: tzparse
    Running setup.py install for tzparse ... done
Successfully installed tzparse-0.2.0

(.venv) D:\work\tzparse>pip install pyinstaller
Processing d:\userarea\j0156585\appdata\local\pip\cache\wheels\57\9a\e0\213da356866201eac897534a77c7af30b48b48c2734e30a25f\pyinstaller-3.6-py3-none-any.whl
Requirement already satisfied: pefile>=2017.8.1 in d:\work\tzparse\.venv\lib\site-packages (from pyinstaller) (2019.4.18)
Requirement already satisfied: setuptools in d:\work\tzparse\.venv\lib\site-packages (from pyinstaller) (41.2.0)
Requirement already satisfied: altgraph in d:\work\tzparse\.venv\lib\site-packages (from pyinstaller) (0.17)
Requirement already satisfied: pywin32-ctypes>=0.2.0 in d:\work\tzparse\.venv\lib\site-packages (from pyinstaller) (0.2.0)
Requirement already satisfied: future in d:\work\tzparse\.venv\lib\site-packages (from pefile>=2017.8.1->pyinstaller) (0.18.2)
Installing collected packages: pyinstaller
Successfully installed pyinstaller-3.6
~~~

Use pyinstaller to build the exe file.

~~~shell
(.venv) D:\work\tzparse>pyinstaller tzparse\cli.py --onefile --name tzparse
77 INFO: PyInstaller: 3.6
78 INFO: Python: 3.8.3
78 INFO: Platform: Windows-10-10.0.18362-SP0
79 INFO: wrote D:\work\tzparse\tzparse.spec
80 INFO: UPX is not available.
82 INFO: Extending PYTHONPATH with paths
['D:\\work\\tzparse', 'D:\\work\\tzparse']
82 INFO: checking Analysis
83 INFO: Building Analysis because Analysis-00.toc is non existent
83 INFO: Initializing module dependency graph...
85 INFO: Caching module graph hooks...
90 INFO: Analyzing base_library.zip ...
2686 INFO: Processing pre-find module path hook   distutils
2687 INFO: distutils: retargeting to non-venv dir 'C:\\Python\\Python3.8\\lib'
5284 INFO: Caching module dependency graph...
5425 INFO: running Analysis Analysis-00.toc
5428 INFO: Adding Microsoft.Windows.Common-Controls to dependent assemblies of final executable
  required by d:\work\tzparse\.venv\scripts\python.exe
5445 INFO: Analyzing D:\work\tzparse\tzparse\cli.py
5816 INFO: Processing pre-find module path hook   site
5817 INFO: site: retargeting to fake-dir 'd:\\work\\tzparse\\.venv\\lib\\site-packages\\PyInstaller\\fake-modules'
8205 INFO: Processing module hooks...
8205 INFO: Loading module hook "hook-distutils.py"...
8208 INFO: Loading module hook "hook-encodings.py"...
8335 INFO: Loading module hook "hook-lib2to3.py"...
8342 INFO: Loading module hook "hook-openpyxl.py"...
8353 INFO: Loading module hook "hook-pkg_resources.py"...
8777 INFO: Processing pre-safe import module hook   win32com
Traceback (most recent call last):
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'win32com'
8851 INFO: Processing pre-safe import module hook   win32com
Traceback (most recent call last):
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'win32com'
9006 INFO: Excluding import '__main__'
9008 INFO:   Removing import of __main__ from module pkg_resources
9009 INFO: Loading module hook "hook-pydoc.py"...
9011 INFO: Loading module hook "hook-sysconfig.py"...
9012 INFO: Loading module hook "hook-xml.dom.domreg.py"...
9013 INFO: Loading module hook "hook-xml.etree.cElementTree.py"...
9014 INFO: Loading module hook "hook-xml.py"...
9016 INFO: Loading module hook "hook-_tkinter.py"...
9216 INFO: checking Tree
9216 INFO: Building Tree because Tree-00.toc is non existent
9217 INFO: Building Tree Tree-00.toc
9294 INFO: checking Tree
9295 INFO: Building Tree because Tree-01.toc is non existent
9295 INFO: Building Tree Tree-01.toc
9334 INFO: Looking for ctypes DLLs
9393 INFO: Analyzing run-time hooks ...
9399 INFO: Including run-time hook 'pyi_rth__tkinter.py'
9400 INFO: Including run-time hook 'pyi_rth_multiprocessing.py'
9405 INFO: Including run-time hook 'pyi_rth_pkgres.py'
9415 INFO: Looking for dynamic libraries
9930 INFO: Looking for eggs
9930 INFO: Using Python library C:\Python\Python3.8\python38.dll
9931 INFO: Found binding redirects:
[]
9937 INFO: Warnings written to D:\work\tzparse\build\tzparse\warn-tzparse.txt
10013 INFO: Graph cross-reference written to D:\work\tzparse\build\tzparse\xref-tzparse.html
10042 INFO: checking PYZ
10042 INFO: Building PYZ because PYZ-00.toc is non existent
10043 INFO: Building PYZ (ZlibArchive) D:\work\tzparse\build\tzparse\PYZ-00.pyz
10927 INFO: Building PYZ (ZlibArchive) D:\work\tzparse\build\tzparse\PYZ-00.pyz completed successfully.
10942 INFO: checking PKG
10942 INFO: Building PKG because PKG-00.toc is non existent
10942 INFO: Building PKG (CArchive) PKG-00.pkg
13621 INFO: Building PKG (CArchive) PKG-00.pkg completed successfully.
13641 INFO: Bootloader d:\work\tzparse\.venv\lib\site-packages\PyInstaller\bootloader\Windows-64bit\run.exe
13641 INFO: checking EXE
13642 INFO: Building EXE because EXE-00.toc is non existent
13644 INFO: Building EXE from EXE-00.toc
13644 INFO: Appending archive to EXE D:\work\tzparse\dist\tzparse.exe
13691 INFO: Building EXE from EXE-00.toc completed successfully.
~~~

Executable should be ready in dist/tzparse.exe

[IANA]:https://www.iana.org/time-zones
