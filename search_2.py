from elasticsearch import Elasticsearch
import re #for regex
import calc_metric_2

#import rating data into Python
ratings=[]
file=open('ratings.csv','r')
file.readline() #skip first line
line=file.readline() #save line into variable
while line: #from each line (each rating)
    line=line.rstrip() #first remove trailling spaces and new line character
    rating=re.findall(r'[^,]+',line) #match strings that do not contain commas
    ratings.append(rating) #put rating in ratings list
    #go to next line
    line=file.readline()
        

#connect to ElasticSearch
es=Elasticsearch([{'host': 'localhost', 'port': 9200}])

#change similarity to BM25
es.indices.close("movies") #close the index
settings={ #create similarity settings
    "index": {
        "similarity": {
            "default": {
                "type": "BM25"
                }
            }
        }
    }
es.indices.put_settings(settings,"movies") #change default similarity settings of index
es.indices.open("movies") #open the index

while(1): #loop for multiple searches
    
    #get search keyword from user
    keyword=input( "\nEnter title keyword:\n" )

    #get user id from user
    user_id=input( "\nEnter user id:\n" )

    #search using keyword in ElasticSearch (max results=10000)
    res=es.search(index='movies', size=10000, body={'query':{'match':{'title':keyword}}})

    #calculate max BM25 score of the results for normalisation
    all_BM25=[]
    for hit in res['hits']['hits']:
        all_BM25.append(hit['_score'])
    max_BM25=max(all_BM25)
    
    #update similarity scores for each movie with custom metric
    for i in range(len(res['hits']['hits'])):
        hit=res['hits']['hits'][i] # temporary variable for readability
        res['hits']['hits'][i]['_score']=calc_metric_2.calc_metric(ratings,user_id,hit['_id'],hit['_score'],max_BM25) #calculate new metric using calc_metric.py

    #sort results based on updated metric in descending order
    res['hits']['hits'].sort(reverse=True,key=lambda x: x['_score'])
        
    #print all the results returned
    print("\nResults found: "+str(len(res['hits']['hits']))+"\n") #show number of results found
    print("id\tscore\tmovie")
    for hit in res['hits']['hits']: #array res['hits']['hits'] contains all results
        output=hit['_id']+"\t"+str(round(hit['_score'],4))+"\t"+hit['_source']['title']+" [ "
        for genre in hit['_source']['genres']:
            output+=genre+" "   
        output+="]"
        print(output) #print movie

    again=input( "\nSearch again?(yes/no):\n" ) #ask to search again

    while(again!='yes' and again!='no'): #while input is invalid
        again=input( "\nPlease enter yes or no:\n" ) #ask for input again

    if(again=='no'):
        break #if no get out of while loop
    
