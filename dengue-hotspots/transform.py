#!/usr/bin/env python

import pyexcel as pe
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pprint
import json
from pymapreduce import Job, RambasedRunner

def int_column(col):
    return lambda row: int(row[col])

def str_column(col):
    return lambda row: row[col]

SCHEMA = {
    u'Year': int_column(1),
    u'Week': int_column(2),
    u'State': str_column(3),
    u'District/Zone/PBT': str_column(4),
    u'Locality': str_column(5),
    u'Total Accumulated Cases': int_column(6),
    u'Length of Outbreak (Days)': int_column(7)
}

# Using MapReduce simply because we can
# 
# yeah i know its overkill

class MapReduce(Job):

    def __init__(self, f):
        self.f = f

    def enumerate(self):
        sheet = pe.get_sheet(file_name=self.f)
        return enumerate(sheet.to_array())

    def reduce_start(self):
        self.d = []

    def reduce_value(self, r):
        self.d.append(r)

    def reduce_stop(self):
        return self.d

    def map(self, item, cb):
        (pos, row) = item
        try:
            result = {}
            for k, f in SCHEMA.items():
                result[k] = f(row)
            cb((pos, result))
        except:
            print "Skipping row %s" % str(row)

runner = RambasedRunner()
dataset = runner.run(MapReduce('MOH_denggue_HOTSPOT_2010_2014_v3.xlsx'))

out = open('dengue-hotspot.json', 'w')
for row in dataset:
    out.write(json.dumps(row) + '\n')
out.close()
