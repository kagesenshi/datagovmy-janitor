import json
#import geocoder
from pymapreduce import Job, RambasedRunner
from fuzzywuzzy import process as fuzzyprocess
import re
import codecs

class ExtractLocations(Job):

    def __init__(self, f):
        self.f = f

    def enumerate(self):
        return enumerate(codecs.open(self.f, 'r', 'utf_8'))

    def map(self, item, cb):
        (pos, data) = item
        d = json.loads(data)
        locality = re.sub(' +', ' ', d['Locality'].strip().replace('\n',', '))
        location = '%s, %s' % (locality, d['State'].strip())
        words = re.compile('\w+').findall(location)
        cb((pos, (location, words)))

    def reduce_start(self):
        self.locations = set()
        self.words = set()

    def reduce_value(self, r):
        (location, words) = r
        self.locations.add(location)
        for w in words:
            self.words.add(w)

    def reduce_stop(self):
        return (list(self.locations), list(self.words))

class FindDuplicates(Job):

    def __init__(self, words):
        self.w = words

    def enumerate(self):
        return enumerate(self.words)

    def map(self, item, cb):
        (pos, data) = item
        similar = fuzzyprocess.extract(item, self.words)
        

runner = RambasedRunner()
(locations, words) = runner.run(ExtractLocations('dengue-hotspot.json'))

for i in sorted(locations):
    print i
