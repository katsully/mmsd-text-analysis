from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords

train = [
    ("Aquafina water tastes bad. Why would my mom buy it?", 'water'),
    ("I hate when I open my camera and I think it's the snapchat camera and I double click and it doesn't switch the camera..", 'camera'),
    ('Trying to watch Netflix and my internet is not cooperating', 'internet'),
    ('I can\'t think of more than three things to put on my Christmas list.', 'Christmas'),
    ("When your card is unknowingly cancelled and is then declined in Starbucks. ", 'coffee'),
    ('My wife\'s getting REALLY angry because the butter is too hard and won\'t spread easily', 'food'),
    ('Boo. Emergency water mains work means we have no clean running water here for a few hours.', 'water'),
    ("Noooooo! The internet is down, which means no Wi-Fi, which means no Netflix, which means I have to find something to do.", 'water'),
    ('When your hands too fat to reach the bottom of the Pringles tube!! ', 'food'),
    ('I dream of a world where I can have a hot shower at the same time my housemates runs the hot tap downstairs ', 'water'),
    ('I know this is one of the most common #firstworldproblems, but not having data on my phone so I can Instagram drives me NUTS.', 'internet'),
    ('When the life of your favorite hair tie is fading away', 'hair'),
    ('True life: I\'m hungry but don\'t know what to eat', 'starving'),
    ('Is there really anything more frustrating than slow internet?', 'internet'),
    ('Comp just had to rage quit when I was in the middle of work. What\'s worse is that there\'s no table that I can flip.', 'computer'),
    ('Forgot my headphones for the bus can I die', 'bus'),
    ('Awkward moment when the only exercise you\'ve done in over a week is running for the train that is then delayed.', 'excercise'),
    ('We can\'t decide where to go on our honeymoon.', 'wedding'),
    ('Forgetting which floor you parked your car on the multi story', 'car'),
    ('oh my god i was rushing out of the house this morning and forgot to brush my teeth i\'m going to die', 'teeth'),
    ('I was devastated when my nexus 4 didn\'t fit in my Louis Vuitton phone case, the same when I ditched my ipad 1', 'cell phone'),
    ('Trying to cut back on the amount of ubers I take is one of the hardest things I\'ve ever done', 'transportation'),
    ('I can\'t get a decent 4g reception around here', 'internet'),
    ('because your closet has become a portal to possibly Narnia and/or the underworld and is chaos', 'clothes'),
    ('I forgot my headphones at home and can\'t listen to music on the train and that is actually the worst.', 'train')
]

test = [
    ("my second home has no hot water", "water")
]
tweets = []
for (words, sentiment) in train:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    filtered_words = [word for word in words_filtered if word not in stopwords.words('english')]
    tweets.append((filtered_words, sentiment))

# print tweets


# create a new classifier by passing training data into the constructor 
cl = NaiveBayesClassifier(tweets)
print "somethin", cl.classify("my second home has no hot water")
cl2 = NaiveBayesClassifier(train)
print cl.accuracy(test)

from textblob import TextBlob
blob = TextBlob("The beer was amazing. "
                "But the hangover was horrible. My boss was not happy.",
                classifier=cl)

print blob.classify()

for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())
# "pos", "neg", "neg"