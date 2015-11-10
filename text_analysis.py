# FINAL VERSION
import random 
from nytimesarticle import articleAPI
import twython

# GET TWEET
with open("twitter_keys.txt") as f:
    content = f.readlines()

# Twitter API keys go here
CONSUMER_KEY = content[0].rstrip()
CONSUMER_SECRET = content[1].rstrip()

OAUTH_TOKEN = content[2].rstrip()
OAUTH_TOKEN_SECRET = content[3].rstrip()

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

response = twitter.search(q='#itpmssd AND [second OR third]', result_type='recent', lang='en', count=1)

first_tweet = response['statuses'][0]
target = first_tweet['user']['screen_name']
targetID = first_tweet['id_str']

## HUGO AND KAT GET TWEET AND GIVE ELI SOME KEYWORD

## GET NEWS ARTICLE
in_file = open('ny_times_key.txt')
key = in_file.read()
in_file.close()
api = articleAPI(key)

developingCountries= ["Mali", "Egypt","China", "Cuba","South Africa", "Algeria","Angola","Bolivia","Brunei","Burma","Chile", "Congo","Ecuador","Fiji","Ghana","Guatemala", "Haiti", "India","Iran", "Iraq", "Kenya", "Lebanon", "Libya", "Malaysia","Mexico","Mongolia", "Nepal", "Peru", "Philippines", "Poland", "Russia", "Somalia", "South Africa", "south Sudan", "Syria","Thailand","Thailand","Turkey", "United Arab", "Ukraine", "Venezuela", "Cuba", "North Korea"]
randomList= random.sample(range(0, len(developingCountries)), 8)

allResults=[]

def queryNYT():
    for i in range (0,len(randomList)): 
        search_number=randomList[i]
        articles =api.search(q = "crisis" , fq = {'headline': developingCountries[search_number] , 'source':['Reuters','AP', 'The New York Times']},begin_date = 20111231)
        
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
        #dic['desk'] = i['news_desk']
        #dic['date'] = i['pub_date'][0:10] # cutting time of day.
        #dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")

        #dic['source'] = i['source']
        #dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        #dic['word_count'] = i['word_count']
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
    #print news[1]["headline"]

headline = news[0].get('headline')
link = news[0].get('url')

## POST TO TWITTER

# link = "www.google.com"
# target_thing = "_blank"
# title = "Headline"
# source_thing = "<a href=%s target=%s>%s</a>" % (link, target_thing, title)
# print source_thing

# code = "We Says Thanks!"
# html = """\
# "<a href=www.google.com target=_blank>hi</a>"
# """.format(code=code)

## this will get updated from eli's code
twitter.update_status(status="@"+target+" "+"Check out this #developingworldproblem: %s %s" % (headline, link), in_reply_to_status_id=targetID)