from elasticsearch import Elasticsearch
import numpy as np #for arrays
import re #for regex
import math #for log()
from sklearn import preprocessing #for data normalization
from sklearn.svm import SVC #for SV Classifier

#connect to ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#get all movie ids from ElasticSearch
movie_ids=[]
res=es.search(index='movies', size=10000, body={'query':{'match_all':{}}})
for hit in res['hits']['hits']: #array res['hits']['hits'] contains all results
        movie_ids.append(hit['_id'])
print('got movies')


#get all movie title terms and movie genres
terms=set()#it is a set to avoid dublicate terms
term_list=[]
genres=set()
genre_list=[]
for movie_id in movie_ids:
    #title terms
    res=es.termvectors(index='movies',id=movie_id,fields='title',term_statistics='true')
    for term in res['term_vectors']['title']['terms']:
        terms.add(term)
    #genres
    res=res=es.search(index='movies', size=10000, body={'query':{'match':{'_id':movie_id}}})
    for genre in res['hits']['hits'][0]['_source']['genres']:
        genres.add(genre)      
term_list=list(terms)
genre_list=list(genres)  
print('got terms and genres')


#create tfidf array (X=movies,Y=terms)
tfidf_array=np.zeros((len(movie_ids),len(term_list)))
for movie_id in movie_ids:
    res=es.termvectors(index='movies',id=movie_id,fields='title',term_statistics='true')
    for term in res['term_vectors']['title']['terms']:
        term_dir=res['term_vectors']['title']['terms'][term] #save term directory for readability
        tf=term_dir['term_freq'] # tf=term_title_appearances
        idf=math.log(res['term_vectors']['title']['field_statistics']['doc_count']/term_dir['doc_freq']) # idf=log(number_of_docs/term_doc_appearances)
        tfidf=tf*idf
        tfidf_array[movie_ids.index(movie_id),term_list.index(term)]=tfidf
print('got tfidf:'+str(tfidf))

#create one hot encoding array (X=movies,Y=genres)
onehot_array=np.zeros((len(movie_ids),len(genre_list)))
for movie_id in movie_ids:
    res=es.search(index='movies', size=10000, body={'query':{'match':{'_id':movie_id}}})
    for genre in res['hits']['hits'][0]['_source']['genres']:
        onehot_array[movie_ids.index(movie_id),genre_list.index(genre)]=1
print('got one hot encoding')

#create data set
dataset=np.concatenate((tfidf_array,onehot_array),1)

#normalise data set by scaling in [0,1]
scaler=preprocessing.MinMaxScaler()
dataset=scaler.fit_transform(dataset)


#import rating data into Python
ratings_list=[]
file=open('ratings.csv','r')
file.readline() #skip first line
line=file.readline() #save line into variable
while line: #from each line (each rating)
    line=line.rstrip() #first remove trailling spaces and new line character
    rating=re.findall(r'[^,]+',line) #match strings that do not contain commas
    ratings_list.append(rating) #put rating in ratings list
    line=file.readline()#go to next line

#insert data to numpy array (makes life easier and readability better)
ratings=np.asarray(ratings_list)


#create train and test dataset for each user and use it for K Nearest Neighbour(k=10)

users=set(ratings[:,0]) #all unique user ids (a set)
i=1 #counter for users for monitoring

for user in users:

        print('\nThis is the '+str(i)+'th user: id '+user)

        #create train dataset user_dataset (rated movies by user)
        user_movies=ratings[:,1][(np.where(ratings[:,0]==user))].tolist() #list of movie ids the user has rated
        user_ratings=ratings[:,2][(np.where(ratings[:,0]==user))].tolist() #list of ratings of movies the user has rated
        user_dataset=np.zeros((len(user_movies),dataset.shape[1])) #init user_dataset array
        for movie in user_movies:
                user_dataset[user_movies.index(movie),:]=dataset[movie_ids.index(movie),:] #add to user_dataset only the samples of the dataset that include movies the user has rated      
        print("created user train dataset")

        #create test dataset not_user_dataset(NOT rated movies by user)
        not_user_movies=[]
        for movie in movie_ids:
                if movie not in user_movies:
                        not_user_movies.append(movie)
        not_user_dataset=np.zeros((len(not_user_movies),dataset.shape[1])) #init not_user_dataset array
        for movie in not_user_movies:
                not_user_dataset[not_user_movies.index(movie),:]=dataset[movie_ids.index(movie),:] #add to not_user_dataset only the samples of the dataset that include movies the user has NOT rated
        print("created user test dataset")
        
        #train SVC
        svc=SVC(gamma='auto')
        svc.fit(user_dataset,user_ratings)
        print("trained SVC")

        #predict ratings with SVC
        not_user_ratings=svc.predict(not_user_dataset)
        print("predicted with SVC")
        
        #add new rating to ratings_list array
        for movie in not_user_movies:
                new_rating=[user,movie,not_user_ratings[not_user_movies.index(movie)],'0'] #timestamp attribute will be zero because we dont care about it
                ratings_list.append(new_rating)        
        print("new ratings added ")
        
        i=i+1 #counts users

#write ratings_list into ratings_4.csv
with open('ratings_4.csv','a') as file:
    for row in ratings_list:
        line=row[0]+","+row[1]+","+row[2]+","+row[3]+"\n"
        file.write(line)                 
                
                           

                           
        
