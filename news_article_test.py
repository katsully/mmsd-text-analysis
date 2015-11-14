import random 
from nytimesarticle import articleAPI
import pandas as pd
import re
import os
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests

## GET NEWS ARTICLE
in_file = open('/Users/Kat/Projects/MSSD/ny_times_key.txt')
key = in_file.read()
in_file.close()
api = articleAPI(key)

developingCountries= ["Mali", "Egypt","China", "Cuba","South Africa", "Algeria","Angola","Bolivia","Brunei","Burma","Chile", "Congo","Ecuador","Fiji","Ghana","Guatemala", "Haiti", "India","Iran", "Iraq", "Kenya", "Lebanon", "Libya", "Malaysia","Mexico","Mongolia", "Nepal", "Peru", "Philippines", "Poland", "Russia", "Somalia", "South Africa", "south Sudan", "Syria","Thailand","Thailand","Turkey", "United Arab", "Ukraine", "Venezuela", "Cuba", "North Korea"]
randomList= random.sample(range(0, len(developingCountries)), 8)

allResults=[]

def queryNYT():
    for i in range (0,len(randomList)): 
        search_number=randomList[i]
        articles =api.search(q = "clean water" , fq = {'headline': developingCountries[search_number] , 'source':['Reuters','AP', 'The New York Times']},begin_date = 20150101)
        
        if len(articles)>0:
            allResults.append(articles)
    
    return allResults


queryNYT()

news = []
for oneSearch in allResults: 
    for i in oneSearch['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        if i['abstract'] is not None:
            dic['abstract'] = i['abstract'].encode("utf8")
        dic['headline'] = i['headline']['main'].encode("utf8")
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")

        dic['url'] = i['web_url']
        # locations
        locations = []
        for x in range(0,len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects   

        news.append(dic)

# test if can access article
news_article = ""
for new in news:
    url = new.get('url')
    print url
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    # do something
    errors = soup.body.findAll(text='Page No Longer Available')
    if not errors:
        news_article = new
        break


def make_tiny(url):

    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    
    print request_url

    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')

headline = news_article.get('headline').decode('utf-8')
link = make_tiny(news_article.get('url'))
print link