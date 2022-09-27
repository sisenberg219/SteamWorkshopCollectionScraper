#TO-DO
#1. Link error checking
#2. Storing a file of each type on each sheet

import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import pandas as pd

urlInput = input('Enter the collection URL: ')
url = urlInput #URL for the collection
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
collectionTitle = soup.find('title').text[16:]

urlList = soup.find_all('div', class_="workshopItem")
nameList = []
sizeList = []
linkList = []
typeList = []

for i in urlList:
    links = i.find_all('a', href=True)
    for link in links:
        tempUrl = link['href']
        tempPage = requests.get(tempUrl)
        tempSoup = BeautifulSoup(tempPage.content, "html.parser")       
        fileSize = tempSoup.find('div', class_="detailsStatRight")
        fileName = tempSoup.find('title')
        fileSoup = tempSoup.find_all('div', class_="workshopTags")
        if (len(fileSoup)) == 1: #if length == 1, the mod does not have an Addon type
            typeList.append('Addon')
        if (len(fileSoup)) > 1:
            typeList.append(fileSoup[1].find('a').text)
        nameString = fileSize.text
        noMB = nameString.replace('MB', '')
        nameList.append(fileName.text[16:])
        sizeList.append(noMB)
        linkList.append(tempUrl)
        

df = pd.DataFrame({'Mod Name': nameList, 'File Size (MB)':  sizeList, 'Mod Type': typeList, 'Link': linkList})
df.to_excel(collectionTitle+'.xlsx', sheet_name='All Mods', index=False)
print('Jobs Done :D')
