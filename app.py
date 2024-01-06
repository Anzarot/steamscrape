import requests
from bs4 import BeautifulSoup
import os
import json
import re
import pandas as pd


link = 'https://store.steampowered.com/app/{appid}/'
head = {'cookie': 'sessionid=cd46137aee87759ca68f1347'}
try:
    startId = pd.read_csv('./gameDatas2.csv',header=None)[0][-1:].item()+10
except:
    startId = 483940
endId = 967892 #2419730

allTags = pd.read_csv('./AllTags.csv',header=None)

allFalseTagDict = {}

for i in range(0,len(allTags)):
    allFalseTagDict.update({allTags.iloc[i].to_string(header=False, index=False):[False]})
    
try:
    os.mkdir('resultfile')
except FileExistsError:
    pass


def get_game(x):

    try:
        linkInstance = link.format(appid=x)
        #print(linkInstance)
        req = requests.get(linkInstance)
        soup = BeautifulSoup(req.text, 'html.parser')
        if soup.find('div', {'class': 'page_background_holder'}) or soup.find('div', {'class': 'game_area_dlc_bubble'}):
            pass
        else:
            writeData(scrapped=scrap(soup=soup,appId=x))
    except:
        pass
    

def writeData(scrapped):
    try:
        df = pd.DataFrame(scrapped)
        df.to_csv('./gameDatas2.csv', mode='a', index=False, header=False)
        print(scrapped["appId"])
        print(" scrapped\n")
    except:
        print("zortladik")

def scrap(soup,appId):
    gameTags = {}
    gameTags.update(allFalseTagDict)
    price = ""
    reviewTag = ""
    reviewCount = 0
    releaseDate = ""
    developers = []
    title = ""
   
#Tags
    try:
        tagDiv = soup.find('div', {'class': 'popular_tags'}).find_all('a')
        for i in tagDiv:
            try:
                gameTags.update({re.sub(r"[\n\t\r]*", "", i.get_text()):[True]})
                
            except:
                pass
    except:
        pass
    
#Price
    try:
        discountPrice = soup.find('div', {'class': 'discount_original_price'}).get_text()
    except:
        pass
    else:
        price = discountPrice

    try:
        noDiscountPrice = soup.find('div', {'class': 'game_purchase_price'}).get_text()
    except:
        pass
    else:
        price = noDiscountPrice
#Reviews
    try:
        allTimeRow= soup.find('div', {'class': 'user_reviews'}).find_all('div',{'class':'user_reviews_summary_row'})[1].find('div',{'class':'summary'})
        reviewTag = allTimeRow.find('span', {'class':'game_review_summary'}).get_text()
        reviewCount= int(re.sub('[^a-zA-Z0-9]', '', allTimeRow.find('span', {'class':'responsive_hidden'}).get_text()[1:-1]))
    except:
        pass
#Release Date
    try:
        releaseDate = soup.find('div', {'class': 'date'}).get_text()
    except:
        pass
#Developer
    try:
        devList = soup.find('div', {'class': 'dev_row'}).find('div',{'id':'developers_list'}).find_all('a')
        for dev in devList:
            developers.append(dev.get_text())
    except:
        pass
    
#Title
    try:
        title = soup.find('div', {'class': 'apphub_AppName'}).get_text()
    except:
        pass
    try:
        rawDict= {  'appId': [appId],
                'title': [title],
                'releaseDate': [releaseDate],
                'developer': [developers][0][0],
                'reviewTag': [reviewTag],
                'reviewCount': [reviewCount],
                'price': [price],
            }
    except:
        pass
    else:
        return merge_dictionaries(rawDict,gameTags)

        
        
def merge_dictionaries(x, y):
    z = x.copy()   
    z.update(y)    
    return z

def run():
    for appid in range(startId,endId,10):
        get_game(appid)

run()
print("bitty")



''' TAGLERI ALMAK ICIN KULLANDIM
def getAllTags():
    alltags = []
    tagreq = requests.get("https://store.steampowered.com/tag/browse/#global_492")
    soup = BeautifulSoup(tagreq.text, 'html.parser')
    allclasses = soup.find('div', {'class': 'tag_browse_tags'}).find_all('div')
    for div in allclasses:
        alltags.append(div.get_text())
    df = pd.DataFrame(alltags)
    df.to_csv('AllTags.csv', mode='w', index=False, header=False)
getAllTags()
'''