# movies-elasticsearch

A simple personalized movie search engine with different ranking implementations (BM25, custom metric, custom metric + clustering imputation).
The custom metric combines avg movie rating, current user rating and relevance (BM25).

Instructions:
1. Run ElasticSearch
2. Run insert_movies.py
3. Run search_1.py / search_2.py  
or  
3. Run create_data_3 (takes a long time, output file here -> https://drive.google.com/file/d/1VDm7z7K32N-Ah-XFUwJ_sKuOmGGOsiHW/view?usp=sharing)
4. Run search_3.py (needs ratings_3.csv)

Information:
* insert_movies.py : Inserts movies.csv data into elasticsearch
* search_1.py : Movie search with ranking based on relevance (BM25 metric)
* search_2.py : Personalised movie search with ranking based on avg movie rating given by users, current user rating and relevance (custom metric)
* cal_metric_2.py : Calculates custom metric for search_2.py
* create_data_3.py : Fills the missing values of the dataset using Support Vector Classification. For the features of the movies the ratings vector and the one-hot encoding vector of title terms is used. 
* search_3.py : Personalised movie search with ranking based on avg movie rating given by similar users (clustering), current user rating and relevance (custom metric).
* calc_metric_3.py : Calculates custom metric for search_3.py
