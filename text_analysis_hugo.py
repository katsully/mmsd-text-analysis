#NLTK
#Naive Bayese clasfier
import nltk

tech_tweets = [('My Samsung smart TV just crashed', 'tecnology'),
              ('When your friends are too scared to take a helicopter to the Hamptons', 'tecnology'),
              ("Please tell me how I can delete 20 pictures and three apps and still don't have room to take any pictures", 'tecnology'),
              ("Where the f is my replacement iPhone6 Can't deal with this iPhone5", 'tecnology'),
              ("I forgot to bring my computer to school and now I'm struggling trying to write an essay draft by hand", 'tecnology'),
              ("No computer until my new charger comes in the mail","tecnology"),
              ("Got into work an hour and a half early to get caught up but found out my work computer is broken" ,"tecnology")]

tv_tweets =  [('Finishing a series on Netflix and not knowing what to do with your life after ', 'television'),
                    ('Hate when you finish an Amazing show on Netflix & have to search for something to match the greatness of the last show', 'television'),
                    ("Truly #firstworldproblems but seriously what's going on @Netflixhelps this is interrupting my binge watching", 'television'),
                    ('Hate when you finish an Amazing show on Netflix & have to search for something to match the greatness of the last show', 'television'),
                    ('It literally stresses me out how much Netflix I have to catch up on ', 'television'),
                    ('Busy day tomorrow , just wanted to sit and watch Netflix all day like a couch potato since I had no school oh well',"television")]


food_tweets =  [("I don't want to eat", 'food'),
                    ("can't find my serial in the new super market", 'food'),
                    ('my bread id not good', 'food'),
                    ('i hate cold meal', 'food'),
                    ('i dont like pasta', 'food')]

# separate each individual word from the tweet that is bigger then 3
all_tweets = []
for (words, sentiment) in tv_tweets + tech_tweets + food_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    all_tweets.append((words_filtered, sentiment))

#print all_tweets

def get_all_words(tweets):
	all_words = []

	for (words,category) in tweets:
		all_words.extend(words)
	
        #print "\n" "\n" "------------ALL WORDS:", all_words
	return all_words


def list_words_by_frequency(wordlist):
 
	freqWordlist = nltk.FreqDist(wordlist)
        print "\n" "\n" "------------fre_list:", freqWordlist
 
        word_freq_list = freqWordlist.keys()

        #print freqWordlist.keys()
	return word_freq_list	

all_unique_words = set(get_all_words(all_tweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in all_unique_words:
        features['contains(%s)' % word] = (word in document_words)
    return features


training_set = nltk.classify.apply_features(extract_features, all_tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

tweet = "Finishing a series on Netflix and not knowing what to do with your life after"
print classifier.classify(extract_features(tweet.split()))


