import twython

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

twitter.update_status(status="@"+target+" "+"hey again!", in_reply_to_status_id=targetID)