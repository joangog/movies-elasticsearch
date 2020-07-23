# elasticsearchproj
A simple movie search engine with different implementations

Instructions:
1. Run ElasticSearch
2. Run insert_movies.py
3. Run search_1.py / search_2.py  
or  
3. Run create_data_3 (takes hours, output file here -> https://drive.google.com/file/d/1VDm7z7K32N-Ah-XFUwJ_sKuOmGGOsiHW/view?usp=sharing)
4. Run search_3.py (needs ratings_3.csv)

Information:
* insert_movies.py : inserts movies.csv data into elasticsearch
* search_1.py : movie search with ranking based on relevance (BM25 metric)
* search_2.py : personalised movie search with ranking based on avg movie rating given by users, current user rating and relevance (custom metric)
* cal_metric_2.py : calculates custom metric for search_2.py
* create_data_3.py : fills the missing values of the dataset using SV classification. For the features of the movies the ratings vector and the one-hot encoding vector of title terms is used. 
* search_3.py : personalised movie search with ranking based on avg movie rating given by similar users (clustering), current user rating and relevance (custom metric).
* calc_metric_3.py : calculates custom metric for search_3.py
