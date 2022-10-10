#TO-DO
#1. Link error checking
#2. Adding relevant data to each sheet

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
gamemodeList = {'modName': [], 'modSize': [], 'modLink': []}
mapList = {'modName': [], 'modSize': [], 'modLink': []}
weaponList = {'modName': [], 'modSize': [], 'modLink': []}
vehicleList = {'modName': [], 'modSize': [], 'modLink': []}
NPCList = {'modName': [], 'modSize': [], 'modLink': []}
toolList = {'modName': [], 'modSize': [], 'modLink': []}
entityList = {'modName': [], 'modSize': [], 'modLink': []}
effectsList = {'modName': [], 'modSize': [], 'modLink': []}
modelList = {'modName': [], 'modSize': [], 'modLink': []}
serverContentList = {'modName': [], 'modSize': [], 'modLink': []}

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
        nameString = fileSize.text
        noMB = nameString.replace('MB', '')

        if (len(fileSoup)) == 1: #if length == 1, the mod does not have an Addon type
            typeList.append('Addon')
        if (len(fileSoup)) > 1:
            fileType = fileSoup[1].find('a').text
            typeList.append(fileType)
            if fileType == 'Gamemode':
                gamemodeList['modName'].append(fileName.text[16:])
                gamemodeList['modSize'].append(noMB)
                gamemodeList['modLink'].append(tempUrl)
            if fileType == 'Map':
                mapList['modName'].append(fileName.text[16:])
                mapList['modSize'].append(noMB)
                mapList['modLink'].append(tempUrl)
            if fileType == 'Weapon':
                weaponList['modName'].append(fileName.text[16:])
                weaponList['modSize'].append(noMB)
                weaponList['modLink'].append(tempUrl)
            if fileType == 'Vehicle':
                vehicleList['modName'].append(fileName.text[16:])
                vehicleList['modSize'].append(noMB)
                vehicleList['modLink'].append(tempUrl)
            if fileType == 'Tool':
                toolList['modName'].append(fileName.text[16:])
                toolList['modSize'].append(noMB)
                toolList['modLink'].append(tempUrl)
            if fileType == 'Entity':
                entityList['modName'].append(fileName.text[16:])
                entityList['modSize'].append(noMB)
                entityList['modLink'].append(tempUrl)
            if fileType == 'Effects':
                effectsList['modName'].append(fileName.text[16:])
                effectsList['modSize'].append(noMB)
                effectsList['modLink'].append(tempUrl)
            if fileType == 'Model':
                modelList['modName'].append(fileName.text[16:])
                modelList['modSize'].append(noMB)
                modelList['modLink'].append(tempUrl)
            if fileType == 'ServerContent':
                serverContentList['modName'].append(fileName.text[16:])
                serverContentList['modSize'].append(noMB)
                serverContentList['modLink'].append(tempUrl)
                
        nameList.append(fileName.text[16:])
        sizeList.append(noMB)
        linkList.append(tempUrl)
        

df = pd.DataFrame({'Mod Name': nameList, 'File Size (MB)':  sizeList, 'Mod Type': typeList, 'Link': linkList})
df.to_excel(writer, sheet_name='All Mods', index=False)

if len(gamemodeList['modName']) > 0:
    modeFrame = pd.DataFrame(gamemodeList)
    modeFrame.to_excel(writer, sheet_name='Gamemode', index=False)
    
if len(mapList['modName']) > 0:
    mapFrame = pd.DataFrame(mapList)
    mapFrame.to_excel(writer, sheet_name='Maps', index=False)

if len(weaponList['modName']) > 0:
    weaponFrame = pd.DataFrame(weaponList)
    weaponFrame.to_excel(writer, sheet_name='Weapons', index=False)

if len(vehicleList['modName']) > 0:
    vehicleFrame = pd.DataFrame(vehicleList)
    vehicleFrame.to_excel(writer, sheet_name='Vehicles', index=False)
    
if len(NPCList['modName']) > 0:
    npcFrame = pd.DataFrame(NPCList)
    npcFrame.to_excel(writer, sheet_name='NPCs', index=False)
    
if len(toolList['modName']) > 0:
    toolFrame = pd.DataFrame(toolList)
    toolFrame.to_excel(writer, sheet_name='Tools', index=False)

if len(entityList['modName']) > 0:
    nameFrame = pd.DataFrame(entityList)
    nameFrame.to_excel(writer, sheet_name='Entities', index=False)
    
if len(effectsList['modName']) > 0:
    effectFrame = pd.DataFrame(effectsList)
    effectFrame.to_excel(writer, sheet_name='Effects', index=False)
    
if len(modelList['modName']) > 0:
    modelFrame = pd.DataFrame.from_dict(modelList)
    modelFrame.to_excel(writer, sheet_name='Effects', index=False)
    
if len(serverContentList['modName']) > 0:
    serverFrame = pd.DataFrame(serverContentList)
    serverFrame.to_excel(writer, sheet_name='Server Content', index=False)

writer.save()
print('Jobs Done :D')
