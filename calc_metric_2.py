def calc_metric(ratings,user_id,movie_id,movie_BM25,max_BM25):
    #inputs:
    #   ratings: list of ratings (each rating is a list of attributes)
    #   user_id: user id
    #   movie_id: movie id
    #   movie_BM25: BM25 similarity score of movie
    #   max_BM25: max BM25 of the movies for normalization
    #output:
    #   the value of the new similarity mnetric

    #initialize
    movie_user_rating=None
    movie_ratings=[]
    avg_rating=None
    
    #get all ratings of movie and specific rating of movie by user
    for row in ratings:
        if row[1]==movie_id:
            movie_ratings.append(float(row[2]))
            if row[0]==user_id:
                movie_user_rating=float(row[2])
    
    #calculate average rating of movie
    if not movie_ratings:
        avg_ratings=None
        
    else:
        avg_rating=sum(movie_ratings)/len(movie_ratings)
    
    #calculate final metric
        
    if movie_user_rating is None and avg_rating is None:
        #print("Movie "+movie_id+": No user rating and average rating found: Calculating metrics using BM25 score...")
        return movie_BM25/max_BM25
    elif movie_user_rating is None:
        #print("Movie "+movie_id+": No user rating found: Calculating metrics using BM25 score and average rating...")
        return (movie_BM25/max_BM25+avg_rating/5)/2
    elif avg_rating is None:
        #print("Movie "+movie_id+": No average rating found: Calculating metrics using BM25 score and user rating...")
        return (movie_BM25/max_BM25+movie_user_rating/5)/2
    else:
        #print("Movie "+movie_id+": Calculating metrics using BM25 score, user rating and average rating.../n")
        return (movie_BM25/max_BM25+movie_user_rating/5+avg_rating/5)/3
    
    

