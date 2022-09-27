#TO-DO
#1. Link error checking
#2. Storing a file of each type on each sheet

import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter


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

#Arrays for specific mod types
gamemode = []
mapList = []
weaponList = []
vehicleList = []
NPCList = []
toolList = []
entityList = []
effectsList = []
modelList = []
serverContent = []

#constructor allowing user to store multiple sheets inside of an excel file
writer = pd.ExcelWriter(collectionTitle+'.xlsx', engine='xlsxwriter')

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
            fileType = fileSoup[1].find('a').text
            typeList.append(fileType)
            if fileType == 'Gamemode':
                gamemode.append(fileName.text[16:])
            if fileType == 'Map':
                mapList.append(fileName.text[16:])
            if fileType == 'Weapon':
                weaponList.append(fileName.text[16:])
            if fileType == 'Vehicle':
                vehicleList.append(fileName.text[16:])
            if fileType == 'Tool':
                toolList.append(fileName.text[16:])
            if fileType == 'Entity':
                entityList.append(fileName.text[16:])
            if fileType == 'Effects':
                effectsList.append(fileName.text[16:])
            if fileType == 'Model':
                modelList.append(fileName.text[16:])
            if fileType == 'ServerContent':
                serverContent.append(fileName.text[16:])
                
        nameString = fileSize.text
        noMB = nameString.replace('MB', '')
        nameList.append(fileName.text[16:])
        sizeList.append(noMB)
        linkList.append(tempUrl)
        

df = pd.DataFrame({'Mod Name': nameList, 'File Size (MB)':  sizeList, 'Mod Type': typeList, 'Link': linkList})
df.to_excel(writer, sheet_name='All Mods', index=False)

if len(gamemode) > 0:
    NPC = pd.DataFrame({'Mod Name': gamemode})
    NPC.to_excel(writer, sheet_name='Gamemode', index=False)
    
if len(mapList) > 0:
    NPC = pd.DataFrame({'Mod Name': mapList})
    NPC.to_excel(writer, sheet_name='Maps', index=False)

if len(weaponList) > 0:
    NPC = pd.DataFrame({'Mod Name': weaponList})
    NPC.to_excel(writer, sheet_name='Weapons', index=False)

if len(vehicleList) > 0:
    NPC = pd.DataFrame({'Mod Name': vehicleList})
    NPC.to_excel(writer, sheet_name='Vehicles', index=False)
    
if len(NPCList) > 0:
    NPC = pd.DataFrame({'Mod Name': NPCList})
    NPC.to_excel(writer, sheet_name='NPCs', index=False)
    
if len(toolList) > 0:
    NPC = pd.DataFrame({'Mod Name': toolList})
    NPC.to_excel(writer, sheet_name='Tools', index=False)

if len(entityList) > 0:
    NPC = pd.DataFrame({'Mod Name': entityList})
    NPC.to_excel(writer, sheet_name='Entities', index=False)
    
if len(effectsList) > 0:
    NPC = pd.DataFrame({'Mod Name': effectsList})
    NPC.to_excel(writer, sheet_name='Effects', index=False)
    
if len(modelList) > 0:
    NPC = pd.DataFrame({'Mod Name': modelList})
    NPC.to_excel(writer, sheet_name='Models', index=False)

if len(serverContent) > 0:
    NPC = pd.DataFrame({'Mod Name': serverContent})
    NPC.to_excel(writer, sheet_name='Server Content', index=False)

writer.save()
print('Jobs Done :D')
