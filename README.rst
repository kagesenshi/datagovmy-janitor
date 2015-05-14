====================
Data.Gov.My Janitor
====================

This repository contains janitorial or data preparation scripts for
transforming data.gov.my datasets into nice neat JSON and OLAP cubes
for analysis purposes purposes

Usage
======

Initializing buildout::

    git clone https://github.com/kagesenshi/datagovmy-janitor.git
    cd datagovmy-janitor
    sh init.sh

Executing script (eg: dengue-hotspots)::

    cd dengue-hotspots/
    ../bin/python transform.py

Catalog
========

**Dengue Hotspots**

This script transforms MOH dengue XLSX file into JSON for further use

- Path: ``dengue-hotspots/``

- Data URL: http://data.gov.my/folders/MOH/MOH_denggue_HOTSPOT_2010_2014_v3.xlsx

- Contributors:

  - Izhar Firdaus <kagesenshi.87@gmail.com>

- TODO:

  - Transform 'locality' field into Long/Lat
