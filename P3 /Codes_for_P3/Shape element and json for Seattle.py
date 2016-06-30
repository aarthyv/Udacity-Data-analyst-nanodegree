# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:53:49 2016

@author: aarthy
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node['type'] = element.tag
        for a in element.attrib:
            if a in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][a] = element.attrib[a]
            elif a in ['lat', 'lon']:
                if 'pos' not in node:
                    node['pos'] = [None, None]
                if a == 'lat':
                    node['pos'][0] = float(element.attrib[a])
                else:
                    node['pos'][1] = float(element.attrib[a])
            else:
                node[a] = element.attrib[a]
                
        for tag in element.iter("tag"):
            if not problemchars.search(tag.attrib['k']):
          # Tags with single colon
                if lower_colon.search(tag.attrib['k']):

            # Single colon beginning with addr
                    if tag.attrib['k'].find('addr') == 0:
                        if 'address' not in node:
                            node['address'] = {}
                        sub_attr = tag.attrib['k'].split(':', 1)
                        node['address'][sub_attr[1]] = tag.attrib['v']

            # All other single colons processed normally
                    else:
                        node[tag.attrib['k']] = tag.attrib['v']

          # Tags with no colon
                elif tag.attrib['k'].find(':') == -1:
                    node[tag.attrib['k']] = tag.attrib['v']

      # Iterate nd children
        for nd in element.iter("nd"):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None
              

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    seattledata = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                seattledata.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return seattledata

def test():
    seattledata = process_map('seattle.xml', pretty = False)
    pprint.pprint(seattledata[0])
if __name__ == '__main__':
    test()