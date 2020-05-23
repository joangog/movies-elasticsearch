from elasticsearch import Elasticsearch
import re #for regex
import codecs #for opening files in utf-8
import unidecode #for removing accents of multilingual words

#connect to ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#create index "movies" (no "genres" data mapping needed because its an array)
mapping={
  "mappings": {
    "properties": {
      "id":    { "type": "integer" },  
      "title":  { "type": "text"  }, 
      }
    }
  }
es.indices.create(index="movies",body=mapping)

#read movies from file and insert into ElasticSearch
file=codecs.open('movies.csv','r',encoding='utf-8')
file.readline() #skip first line
line=file.readline() #save line into variable

while line: #from each line (each movie)

    line=line.rstrip() #first remove trailling spaces and new line character
    movie=re.findall(r'".+"|[^,]+',line) #match strings that are enclosed in quotes or do not contain commas
    for i in range(len(movie)): movie[i]=re.sub('"','',movie[i]) #remove quotes
    
    #strings matched will be each attribute of the movie

    #save each attribute in variables
    id=movie[0]
    title=unidecode.unidecode(movie[1]) #remove multilingual accents
    genres=movie[2].split('|') #split the attribute "genres" on each "|" and create a list containing each genre

    #insert document movie_info into index "movies" in ElasticSearch
    movie_info={
        "title": title,
        "genres": genres,
        }
    
    res=es.index(index='movies',id=id, body=movie_info)
    
    #go to next line
    line=file.readline() 


