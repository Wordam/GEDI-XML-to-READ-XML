import sys,glob, argparse
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from collections import defaultdict
from xml.dom import minidom

childList = defaultdict(list)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def buildChildList(files,gedi_type):
    for f in files:
        tree = ET.parse(f)
        root = tree.getroot()[1][0]
        for child in root:
            if child.attrib['gedi_type']==gedi_type:
                childList[f].append(child)

def createREADXML(datasetName,attribName,outfile):
    top = Element('wordLocations')
    top.attrib['dataset']=datasetName

    for f in childList:
        for c in childList[f]:
            child = SubElement(top, 'spot')
            child.attrib['x'] = c.attrib['col']
            child.attrib['y'] = c.attrib['row']
            child.attrib['h'] = c.attrib['width']
            child.attrib['w'] = c.attrib['height']
            child.attrib['word'] = c.attrib[attribName]
            child.attrib['image'] = f
    file = open(outfile,"w")
    file.write(prettify(top))

def main(xmlFolder, datasetName, geditype, attribName, outfile):
        files = glob.glob(xmlFolder+"/*.xml")
        buildChildList(files,geditype)
        createREADXML(datasetName,attribName, outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert GEDI XML file folder to a single XML in READ format.')
    parser.add_argument('--xmlFolder', '-f', type=str, required=True,
                                   help='Path to the folder containing the gedi xmls')
    parser.add_argument('--datasetName', '-d', action='store', type=str, required=True,
                                   help='Name of the dataset')
    parser.add_argument('--geditype', '-g', type=str, required=True,
                                   help='Value of attribute gedi_type to select')
    parser.add_argument('--attribName', '-a', action='store', type=str, required=True,
                                   help='Name of the attribute containing the tag value')
    parser.add_argument('--outfile', '-o' ,action='store', type=str, required=True,
                                   help='Path to the output XML file in READ format')
    args = vars(parser.parse_args())
    main(**args)
