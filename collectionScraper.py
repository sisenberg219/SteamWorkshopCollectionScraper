import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import pandas as pd

urlInput = input('Enter the collection URL.')
url = "urlInput" #URL for the collection
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")


urlList = soup.find_all('div', class_="workshopItem")
nameList = []
sizeList = []
linkList = []

for i in urlList:
    links = i.find_all('a', href=True)
    for link in links:
        tempUrl = link['href']
        tempPage = requests.get(tempUrl)
        tempSoup = BeautifulSoup(tempPage.content, "html.parser")
        
        fileSize = tempSoup.find('div', class_="detailsStatRight")
        fileName = tempSoup.find('title')
        nameString = fileSize.text
        noMB = nameString.replace('MB', '')
        nameList.append(fileName.text[16:])
        sizeList.append(noMB)
        linkList.append(tempUrl)



df = pd.DataFrame({'Mod Name': nameList, 'File Size (MB)':  sizeList, 'Link': linkList})
df.to_excel('Mods.xlsx', sheet_name='Mods', index=False)
print('Jobs Done :D')
