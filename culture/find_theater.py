import pandas as pd
import xml.etree.ElementTree as ET
import sys
from urllib.request import urlopen
from xml.etree.ElementTree import parse

url = "http://175.125.91.94/oasis/service/rest/meta10/get20150042?numOfRows=170"
response = urlopen(url).read()
xtree = ET.fromstring(response)
element = xtree.findall('body/items/item')


theater_list = []

for item in element:
    one_list = []
    title = item.find('title').text
    description = item.find('description').text
    # createDate = item.find('createDate').text
    # creator = item.find('creator').text
    # extent = item.find('extent').text
    # temporal = item.find('temporal').text
    # time = item.find('time').text
    # medium = item.find('medium').text
    # period = item.find('period').text
    # person = item.find('person').text
    referenceIdentifier = item.find('referenceIdentifier').text
    rights = item.find('rights').text
    subjectCategory = item.find('subjectCategory').text
    url = item.find('url').text
    # subjectKeyword = item.find('subjectKeyword').text
    one_list.append(title)
    one_list.append(description)
    # one_list.append(createDate)
    # one_list.append(creator)
    # one_list.append(extent)
    # one_list.append(temporal)
    # one_list.append(time)
    # one_list.append(medium)
    # one_list.append(period)
    # one_list.append(person)
    one_list.append(referenceIdentifier)
    one_list.append(rights)
    one_list.append(subjectCategory)
    one_list.append(url)
    # one_list.append(subjectKeyword)
    theater_list.append(one_list)

    



dataframe = pd.DataFrame(theater_list)
dataframe.to_csv("theater.csv", encoding='cp949', index=False, header=['title', 'description', 'referenceIdentifier', 'rights', 'subjectCategory', 'url'])
