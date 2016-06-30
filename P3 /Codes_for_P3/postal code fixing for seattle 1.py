# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 11:02:43 2016

@author: aarthy
"""

import xml.etree.cElementTree as ET
import re
import pprint


OSMFILE = "seattle.osm.xml"
# 5 or 9 digit codes
VALID_CODE = re.compile('\d\d\d\d\d')

def all_postcode(osmfile):
    """Returns dictionaries of valid and invalid postal codes; original values as dictionary keys, fixed values as values."""
    osm_file = open(osmfile, "r")
    valid = []
    invalid = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == 'node':
            for tag in elem.iter('tag'):
                k = tag.get('k')
                if k == "addr:postcode":
                    v = tag.get('v')
                    if VALID_CODE.match(v):
                        if v not in valid:
                            valid.append(v)
                    else:   
                        invalid.append(v)                    
    return valid, invalid
 

                    
def test():
    """Prints a report about valid and invalid postal codes to stdout."""
    valid, invalid = all_postcode(OSMFILE)
    print "valid postcodes:"
    pprint.pprint(valid)
    print "Number of valid postcodes:", len(valid)
    print "invalid postcodes:"
    pprint.pprint(invalid)
    print "Number of valid postcodes:", len(invalid)
  
if __name__ == '__main__':
    test()
