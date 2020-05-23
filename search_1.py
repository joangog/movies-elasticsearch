from elasticsearch import Elasticsearch

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

    #search using keyword in ElasticSearch (max results=10000)
    res=es.search(index='movies', size=10000, body={'query':{'match':{'title':keyword}}})

    #calculate max BM25 score of the results for normalisation
    all_BM25=[]
    for hit in res['hits']['hits']:
        all_BM25.append(hit['_score'])
    max_BM25=max(all_BM25)
    
    #print all the results returned
    print("\nResults found: "+str(len(res['hits']['hits']))+"\n") #show number of results found
    print("id\tscore\tmovie")
    for hit in res['hits']['hits']: #array res['hits']['hits'] contains all results
        output=hit['_id']+"\t"+str(round(hit['_score']/max_BM25,4))+"\t"+hit['_source']['title']+" [ "
        for genre in hit['_source']['genres']:
            output+=genre+" "    
        output+="]"
        print(output) #print movie

    again=input( "\nSearch again?(yes/no):\n" ) #ask to search again

    while(again!='yes' and again!='no'): #while input is invalid
        again=input( "\nPlease enter yes or no:\n" ) #ask for input again

    if(again=='no'):
        break #if no get out of while loop
    
