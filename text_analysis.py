# FINAL VERSION
import random 
from nytimesarticle import articleAPI
import twython
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
import re
import os

# GET TWEET
with open("/Users/Kat/Projects/MSSD/twitter_keys.txt") as f:
    content = f.readlines()

# Twitter API keys go here
CONSUMER_KEY = content[0].rstrip()
CONSUMER_SECRET = content[1].rstrip()

OAUTH_TOKEN = content[2].rstrip()
OAUTH_TOKEN_SECRET = content[3].rstrip()

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

response = twitter.search(q='#firstworldproblems AND [worst OR ruined OR dying OR worse OR hate OR annoying]', result_type='recent', lang='en', count=1)

first_tweet = response['statuses'][0]
first_world_tweet = first_tweet.get('text')
target = first_tweet['user']['screen_name']
# target = "HugoLuc"
targetID = first_tweet['id_str']
# targetID = 1400173975

## use naive bayes classifier to classify the tweet
trainingSet = []

csvFile = pd.read_csv("/Users/Kat/Projects/MSSD/Training_test/training.csv", low_memory=False, encoding='ISO-8859-1')

for i in range(len(csvFile["tweets"])):
    trainingSet.append((csvFile["tweets"][i],csvFile["category"][i]))

# break up tweets into lists of words, take out stopwords
tweets = []
for (words, sentiment) in trainingSet:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    filtered_words = [word for word in words_filtered if word not in stopwords.words('english')]
    tweets.append((filtered_words, sentiment))

# create a new classifier by passing training data into the constructor 
cl = NaiveBayesClassifier(tweets)
search_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",first_world_tweet).split())
print search_tweet
search_term = cl.classify(search_tweet)
print search_term

if search_term == 'food':
    search_term = 'hunger'
elif search_term == 'water':
    search_term = 'clean water'
elif search_term == 'hygiene':
    search_term = 'health'
elif search_term == 'technology':
    search_term = 'access to technology'

## GET NEWS ARTICLE
in_file = open('/Users/Kat/Projects/MSSD/ny_times_key.txt')
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

headline = news[0].get('headline').encode('utf-8')
link = news[0].get('url')

## POST TO TWITTER

## create status
# headline_total = 137 - len("@"+target+" "+"Check out this #developingworldproblem: %s " % link)
status = "@"+target+" "+"Check out this #developingworldproblem: %s %s" % (headline, link)
# if len(status) > 140:
#     headline = headline[:headline_total] + "..."
#     status = "@"+target+" "+"Check out this #developingworldproblem: %s %s" % (headline, link)
# print status
# post status as reply to original tweeter
twitter.update_status(status=status, in_reply_to_status_id=targetID)
