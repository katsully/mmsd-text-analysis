import twython

# Twitter API keys go here
CONSUMER_KEY = 'g6SmnVniAR0rVCHBWapu7ssX8'
CONSUMER_SECRET = 'wOIXruS0b4UmhzeL7DUkmS4B2avkEAjyiXLcmVgaVuyJEA3M1O'

OAUTH_TOKEN = '104565604-R6kibEf2lYsMG8fbRJyZ9JWZ7KHd1wNKUsJAd8VV'
OAUTH_TOKEN_SECRET = 'HszsWiaEMDrDjJrf4htgVW1nXG2SiFV3UlR4KTO1qWHbg'

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

response = twitter.search(q='#itpmssd AND [second OR third]', result_type='recent', lang='en', count=1)

first_tweet = response['statuses'][0]
target = first_tweet['user']['screen_name']
targetID = first_tweet['id_str']

twitter.update_status(status="@"+target+" "+"hey again!", in_reply_to_status_id=targetID)