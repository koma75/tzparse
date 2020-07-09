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

[IANA]:https://www.iana.org/time-zones