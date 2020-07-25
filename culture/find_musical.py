import pandas as pd
import xml.etree.ElementTree as ET
import sys
from urllib.request import urlopen
from xml.etree.ElementTree import parse

url = "http://175.125.91.94/oasis/service/rest/meta10/get20150045?numOfRows=86"
response = urlopen(url).read()
xtree = ET.fromstring(response)
element = xtree.findall('body/items/item')


musical_list = []

for item in element:
    one_list = []
    title = item.find('title').text
    description = item.find('description').text
    referenceIdentifier = item.find('referenceIdentifier').text
    rights = item.find('rights').text
    subjectCategory = item.find('subjectCategory').text
    url = item.find('url').text
    one_list.append(title)
    one_list.append(description)
    one_list.append(referenceIdentifier)
    one_list.append(rights)
    one_list.append(subjectCategory)
    one_list.append(url)
    musical_list.append(one_list)

dataframe = pd.DataFrame(musical_list)
dataframe.to_csv("musical.csv", encoding='cp949', index=False, header=['title', 'description', 'referenceIdentifier', 'rights', 'subjectCategory', 'url'])
