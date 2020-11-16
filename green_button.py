import os
from lxml import etree
import datetime
from collections import defaultdict

def get_files(directory, extension):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.' + extension)]

def parse_xml(content):
    return etree.XML(content)

def node_to_datapoint(node):
    start = int(node.xpath(".//*[name()='start']")[0].text)
    duration = int(node.xpath(".//*[name()='duration']")[0].text)
    value = int(node.xpath(".//*[name()='value']")[0].text)
    return (start, duration, value)

def load_sce_data_from_xml(contents, tz):
    datapoints = [node_to_datapoint(node)
                    for content in contents
                    for node in parse_xml(content).xpath("//*[name()='IntervalReading']")]
    
    datadict = defaultdict(float)
    dates = set()
    for p in datapoints:
        start, duration, value = p
        assert duration == 900
        ts = datetime.datetime.fromtimestamp(start, tz)
        tsdate = ts.date()
        tstime = ts.hour * 4 + ts.minute // 15
        assert 0 <= tstime <= 95
        datadict[(tsdate, tstime)] = value
        dates.add(tsdate)

    return datadict, dates

