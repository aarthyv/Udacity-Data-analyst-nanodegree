# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:05:39 2016

@author: aarthy
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "seattle.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "st": "Street",
            "Ave": "Avenue",
            "AVE": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Pkwy S.E.": "Parkway SouthEast",
            "Blvd": "Boulevard",
            "Pl N": "Place North",
            "Hwy": "Highway",
            "Dr": "Drive",
            "Rd.": "Road",
            "ave se": "Avenue SouthEast",
            "ave ne": "Avenue NorthEast",
            "Ave. N.E.": "Avenue NorthEast",
            "av" : "Avenue",
            "Av" : "Avenue",
            "Ave N": "Avenue North",
            "Ave NW": "Avenue NorthWest",
            "NE": "NorthEast",
            "NW": "NorthWest",
            "SE": "SouthEast",
            "SW": "SouthWest",
            "E": "East",
            "W": "West",
            "N.": "North",
            "S": "South",
            "Ct": "Court"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    other_street_types = []
    if m:
        street_type= m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type,mapping[street_type],name)
        else:
            other_street_types.append(street_type)
    # only fix the street types that are keys of your mapping dictionary
    # capture all of the other street types and print them outside the loop,
    # so you can extend your mapping dictionary
    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
        print name, "=>", better_name
if __name__ == '__main__':
    test()