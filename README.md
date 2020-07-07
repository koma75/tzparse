tzparse
========================================================================

Command line tool to parse [IANA tzdata][IANA]
for the latest time zone information.

Installation
------------------------------------------------------------------------

~~~shell
> pip install https://github.com/koma75/tzparse
~~~

Usage
------------------------------------------------------------------------

Design Concept
------------------------------------------------------------------------

### Basics

The tool will read data from the [IANA tzdata][IANA] and output two CSV
files.  One CSV should contain a merged list of time-zones with country
names, timezone base offset, applied rule and the time-zone name.
Another CSV should contain all the rules merged from the database.

### Input format

* zone.tab
    * File containing the base list of time-zone and country.  Used as the
        base of the output list
* iso3166.tab
    * File containing the country code to country name conversion list.
* definition files (file names with regions such as africa, asia etc.)
    * File containing the actual time zone definitions with following 
        tags.
        * Zone
        * Actual Zone definition.  Mostly multi-line.
        * If multi-line, the final line should be used to get the latest
            definition.
        * linked rules are also included.
        * Link
        * Link definition to link a zone to another zone.
        * Zone defined with this definition should refer to the linked zone
        * Rule
        * Definition of the daylight saving time rule.  refered frrom each zone

### Output format

Two output files will be created

* zones.csv
    * Country
        * Country name derived from the iso3166.tab file
        * e.g. Japan
    * Zone
        * Zone list obtained from zone.tab file
        * e.g. Asia/Tokyo
    * STDOFF
        * Standard offset defined in each zone definition
        * e.g. 9:00
    * RULE
        * Rule name linked to the zone.
        * e.g. Japan
* rules.csv
    * Rule
        * Name of the Rule
    * FROM
        * Date the rule is applied from
        * e.g. 1982
    * TO
        * Date the rule is applied to
        * e.g. 1983, only (same as FROM), max (MAX_INT)
    * IN
        * Month the switch rule is applied
    * ON
        * Date rule the switch is applied
    * AT
        * Time the switch happenes
    * SAVE
        * Hour offset applied at the timing

### Process flow

1. Parse the iso3166.tab file to get translation list for the country code
   to country name.
    * Hold the translation data in a Key-Value data.
2. Parse all zone list file for all Zones
    * Hold the Zone information data with Key=Zone name and Value containing all other Zone definition.
3. Parse all zone list file for all Links
    * Copy the Zone information of the linked zone to the defined zone.
    * Links are always after the original Zone def. so can be parsed in one flow
4. Parse all zone list file for all Rules and create rules.csv file
    * Can be parsed along with Zones and links
5. Parse Zone.tab and construct the zones.csv file

Input to the Program should include following:

* Folder path containing the tzdata files
* List of zone data file names to read the zone information
    * africa
    * antarctica
    * asia
    * australasia
    * backward
        * not needed.  only used to link old zone names to current ones.
    * backzone
        * unnecessary?
    * etcetera
        * not needed. mostly common names like GMT UTC etc.
    * europe
    * northamerica
    * pacificnew
        * Probably not needed
    * southamerica

[IANA]:https://www.iana.org/time-zones