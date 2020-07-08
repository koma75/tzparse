tzparse
========================================================================

Command line tool to parse [IANA tzdata][IANA]
for the latest time zone information.

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

~~shell
Usage: tzparse [OPTIONS] TZDIR

  IANA timezone database parser.

Options:
  -c, --config <cfg>   Configuration File (default: config.yml)
  -z, --zones <zones>  zone csv output file (default: zones.csv)
  -r, --rules <rules>  rule csv output file (default: rules.csv)
  -o, --overwrite      overwrite output files (default: False)
  -v, --verbose        output in verbose mode
  --version            Show the version and exit.
  --help               Show this message and exit.
~~

Prepare a config file that specify which files to read from
the tzdata folder (example below), and specify the file using --config
option.

~~yaml
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
~~

Execute the command by specifying the directory which you downloaded
earlier.
TZDIR argument and the --config option is mandatory.
Other options may be specified to change certain operations.

[IANA]:https://www.iana.org/time-zones