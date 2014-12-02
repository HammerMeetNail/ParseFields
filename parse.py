from xml.etree import ElementTree as ET
import os
from config import PDF, DEST, DUMPPDF, TEXT, FIXED


# Pulls XML data from PDF and outputs as out.xml
def getPDF():
    if len(PDF) > 1:
        pdf = PDF
    else:
        pdf = raw_input("Please type in a file location: ")
    os.system("{0} {1} > {2}".format(DUMPPDF, pdf, DEST))

# Replaces bad characters in XML
def fixData():
    raw = open(DEST)
    fixed = open(FIXED,"w")
    bad = ["&#"]
    for line in raw:
        for item in bad:
            line = line.replace(item, "BAD XML")
            fixed.write(line)
    fixed.close()
    raw.close()

# Creates XML Tree and returns dictionary with PDF field names and field text
def parseTree():
    tree = ET.parse(FIXED)
    nodeKey = ""
    nodeValue = ""
    fields = {}
    temp = {}

    for node in tree.iter():
        if nodeKey == "FoundKey":
            for child in node.iter():
                if child.tag == "string":
                    temp["Key"] = child.text
            nodeKey = ""
        if node.tag == "key" and node.text == "T":
            nodeKey = "FoundKey"

        if nodeValue == "FoundValue":
            for child in node.iter():
                if child.tag == "string" and "Key" in temp:
                    key = temp["Key"]
                    fields[key] = child.text
                    temp = {}
            nodeValue = ""
        if node.tag == "key" and node.text == "V":
            nodeValue = "FoundValue"
    return fields

# Initiates data extraction and outputs all PDF field names and field values as text
def main():

    getPDF()
    fixData()
    dictItems = parseTree()
    pdfText = open(TEXT, "w")
    # for i in natsorted(dictItems):
    #     pdfText.write(str(i) + ': ' + str(dictItems[i]) + '\n')
    for i in dictItems:
        pdfText.write(str(i) + ': ' + str(dictItems[i]) + '\n')
    pdfText.close()

if __name__ == '__main__':
    main()
