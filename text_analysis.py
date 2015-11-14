# FINAL VERSION
import random 
from nytimesarticle import articleAPI
import twython
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
import re
import contextlib
import HTMLParser
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

# GET TWEET
with open("twitter_keys.txt") as f:
    content = f.readlines()

# Twitter API keys go here
CONSUMER_KEY = content[0].rstrip()
CONSUMER_SECRET = content[1].rstrip()

OAUTH_TOKEN = content[2].rstrip()
OAUTH_TOKEN_SECRET = content[3].rstrip()

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


response = twitter.search(q='#firstworldproblems AND [worst OR ruined OR dying OR worse OR hate OR annoying OR pissed OR annoyed OR panic OR suffering OR distraught OR bitch OR damn OR fucking OR fucked OR hell OR starving]', result_type='recent', lang='en', count=1)

first_tweet = response['statuses'][0]
first_world_tweet = first_tweet.get('text')
target = first_tweet['user']['screen_name']
# target = "HugoLuc"
targetID = first_tweet['id_str']
# targetID = 1400173975

## use naive bayes classifier to classify the tweet
trainingSet = []

csvFile = pd.read_csv("Training_test/training.csv", low_memory=False, encoding='ISO-8859-1')

for i in range(len(csvFile["tweets"])):
    trainingSet.append((csvFile["tweets"][i],csvFile["category"][i]))

# break up tweets into lists of words, take out stopwords
tweets = []
for (words, sentiment) in trainingSet:
    words_filtered = [word.lower() for word in words.split() if len(word) >= 3 and word not in stopwords.words('english')]
    # filtered_words = [word for word in words_filtered if word not in stopwords.words('english')]
    tweets.append((words_filtered, sentiment))

# create a new classifier by passing training data into the constructor 
cl = NaiveBayesClassifier(tweets)
search_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",first_world_tweet).split())
search_term = cl.classify(search_tweet)

if search_term == 'food':
    search_term = 'hunger'
elif search_term == 'water':
    search_term = 'clean water'
elif search_term == 'hygiene':
    search_term = 'health'
elif search_term == 'technology':
    search_term = 'access to technology'

## GET NEWS ARTICLE
in_file = open('ny_times_key.txt')
key = in_file.read()
in_file.close()
api = articleAPI(key)

developingCountries= ["Mali", "Egypt","China", "Cuba","South Africa", "Algeria","Angola","Bolivia","Brunei","Burma","Chile", "Congo","Ecuador","Fiji","Ghana","Guatemala", "Haiti", "India","Iran", "Iraq", "Kenya", "Lebanon", "Libya", "Malaysia","Mexico","Mongolia", "Nepal", "Peru", "Philippines", "Poland", "Russia", "Somalia", "South Africa", "south Sudan", "Syria","Thailand","Thailand","Turkey", "United Arab", "Ukraine", "Venezuela", "Cuba", "North Korea"]
randomList= random.sample(range(0, len(developingCountries)), 8)

allResults=[]

def queryNYT(search_term):
    for i in range (0,len(randomList)): 
        search_number=randomList[i]
        articles =api.search(q = search_term , fq = {'headline': developingCountries[search_number] , 'source':['Reuters','AP', 'The New York Times']},begin_date = 20150101)
        
        if len(articles)>0:
            allResults.append(articles)
    
    return allResults


queryNYT(search_term)

news = []
for oneSearch in allResults: 
    for i in oneSearch['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['url'] = i['web_url']
        news.append(dic)

# test if can access article
news_article = ""
for new in news:
    url = new.get('url')
    # print url
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

# headline = news_article.get('headline').decode('utf-8')
hparser=HTMLParser.HTMLParser()
print news_article
headline=hparser.unescape(news_article.get('headline'))
link = make_tiny(news_article.get('url'))

## POST TO TWITTER

## create status
status = "@"+target+" "+"Check out this #developingworldproblem: %s %s" % (headline, link)
if len(status) > 140:
    headline_total = 137 - len("@"+target+" "+"Check out this #developingworldproblem: %s " % link)
    headline = headline[:headline_total] + "..."
    status = "@"+target+" "+"Check out this #developingworldproblem: %s %s" % (headline, link)
print status

# post status as reply to original tweeter
twitter.update_status(status=status, in_reply_to_status_id=targetID)