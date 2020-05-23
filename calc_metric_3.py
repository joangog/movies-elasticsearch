def calc_metric(dataset,clusters,users,movies,user_id,movie_id,movie_BM25,max_BM25):
    #inputs:
    #   dataset: user-movie rating array which is the kmeans dataset
    #   clusters: the clusters returned by kmeans
    #   users: all user ids
    #   movies: all movie ids
    #   user_id: user id
    #   movie_id: movie id
    #   movie_BM25: BM25 similarity score of movie
    #   max_BM25: max BM25 of the movies for normalization

    #output:
    #   the value of the new similarity mnetric

    #initialize
    movie_user_rating=None
    cluster_ratings=[]
    avg_cluster_rating=None
    
    #get specific rating of movie by user
    movie_user_rating=dataset[int(user_id)-1,movies.index(movie_id)]
    
    #calculate average rating of movie in user's cluster
    user_cluster=clusters[users.index(user_id)]
    for c in clusters: #for every user's cluster categorization returned by kmeans
        if c==user_cluster: #if it the same to the current user's cluster
            matched_user=users[clusters.index(c)]#remember the user whose cluster matched
            cluster_ratings.append(dataset[int(matched_user)-1,movies.index(movie_id)])#add his rating to cluster ratings
    if not cluster_ratings:
        avg_cluster_ratings=None
    else:
        avg_cluster_rating=sum(cluster_ratings)/len(cluster_ratings) #calculate average cluster rating


    #calculate final metric
        
    if movie_user_rating is None and avg_cluster_rating is None:
        #print("Movie "+movie_id+": No user rating and average cluster rating found: Calculating metrics using BM25 score...")
        return movie_BM25/max_BM25
    elif movie_user_rating is None:
        #print("Movie "+movie_id+": No user rating found: Calculating metrics using BM25 score and average cluster rating...")
        return (movie_BM25/max_BM25+avg_cluster_rating/5)/2
    elif avg_cluster_rating is None:
        #print("Movie "+movie_id+": No average cluster rating found: Calculating metrics using BM25 score and user rating...")
        return (movie_BM25/max_BM25+movie_user_rating/5)/2
    else:
        #print("Movie "+movie_id+": Calculating metrics using BM25 score, user rating and average rating.../n")
        return 0.5*movie_BM25/max_BM25+0.3*movie_user_rating/5+0.2*avg_cluster_rating/5
    
    

