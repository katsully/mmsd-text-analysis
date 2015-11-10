import random 
from nytimesarticle import articleAPI
#api = articleAPI('d661f67d9b3ad99e43711924e51432dd:14:70159858')
in_file = open('ny_times_key.txt')
key = in_file.read()
in_file.close()
api = articleAPI(key)

developingCountries= ["Mali", "Egypt","China", "Cuba","South Africa", "Algeria","Angola","Bolivia","Brunei","Burma","Chile", "Congo","Ecuador","Fiji","Ghana","Guatemala", "Haiti", "India","Iran", "Iraq", "Kenya", "Lebanon", "Libya", "Malaysia","Mexico","Mongolia", "Nepal", "Peru", "Philippines", "Poland", "Russia", "Somalia", "South Africa", "south Sudan", "Syria","Thailand","Thailand","Turkey", "United Arab", "Ukraine", "Venezuela", "Cuba", "North Korea"]
randomList= random.sample(range(0, len(developingCountries)), 8)
print randomList
    
allResults=[]

def queryNYT():
    for i in range (0,len(randomList)): 
        search_number=randomList[i]
        articles =api.search(q = "crisis" , fq = {'headline': developingCountries[search_number] , 'source':['Reuters','AP', 'The New York Times']},begin_date = 20111231)
        
        if len(articles)>0:
            allResults.append(articles)
    
    return allResults


queryNYT()
#len(allResults[1])

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

print(news[0])
#print news


