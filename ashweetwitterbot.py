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

link = "www.google.com"
target_thing = "_blank"
title = "Headline"
source_thing = "<a href=%s target=%s>%s</a>" % (link, target_thing, title)
print source_thing

code = "We Says Thanks!"
html = """\
"<a href=www.google.com target=_blank>hi</a>"
""".format(code=code)

## this will get updated from eli's code
twitter.update_status(status="@"+target+" "+"Check out this #developingworldproblem %s" % source_thing, in_reply_to_status_id=targetID)