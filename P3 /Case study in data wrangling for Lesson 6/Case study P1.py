import xml.etree.cElementTree as ET
import pprint
filename = "seattle.xml"
tags = {}
for event, element in ET.iterparse(filename):
    if element.tag in tags:
        tags[element.tag] += 1
    else:
        tags[element.tag] = 1
pprint.pprint(tags)