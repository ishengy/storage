# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:57:27 2019

@author: ivan.sheng
"""
from __future__ import division
from bs4 import BeautifulSoup 
import re
import pandas as pd 
import os
import time

from selenium import webdriver

import nltk
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords 
from gensim import corpora, models
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import copy
import pickle
##nltk.download('wordnet')


df = #dataframe

lemmatizer = WordNetLemmatizer()
remove = ['https', 'http','&amp','amp', 'www', 'com', 'http', 'images', 'uri', 'original', 'reddit','youtube','likes','replies', 'url', 'amazonaws', 'wikipedia', 'org','wiki',"spoiler"]
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(remove)
stop_words = set(stopwords) 

lemma = []
#change 'post' to whatever column holds your text
for story in df.post:
    word_list = nltk.word_tokenize(str(story))
    filtered_sentence = [w for w in word_list if not w in stop_words] 
    lemma_out = ' '.join([lemmatizer.lemmatize(w) for w in filtered_sentence])
    lemma.append(lemma_out)

df['Lemmatized'] = lemma

# Toeknize, Romove puctuation, Words less than 3 letters
def tokenize(text):
    return re.findall("[a-z']{3,}",text.lower()) 

formatted = combine['Lemmatized'].apply(lambda x: tokenize(x))

# BoW + TF-IDF
dictionary = corpora.Dictionary(formatted)
corpus = [dictionary.doc2bow(tokens) for tokens in formatted] # Count words in each row, each word has a unique index
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

# LDA
# Determine best number of clusters
def compute_coherence_values(dictionary, tfidf_corpus, corpus, start, stop, step):
    """
    Input   : dictionary : Gensim dictionary
              corpus : Gensim corpus
              texts : List of input texts
              stop : Max num of topics
    purpose : Compute c_v coherence for various number of topics
    Output  : model_list : List of LSA topic models
              coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for number_of_topics in range(start, stop, step):
        # generate LDA model
        print(number_of_topics)
        lda = models.LdaModel(tfidf_corpus, num_topics=number_of_topics, id2word = dictionary)  # train model
        model_list.append(lda)
        coherencemodel = models.CoherenceModel(model=lda, texts=formatted, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return coherence_values

# Plot coherence chart
cv = compute_coherence_values(dictionary, tfidf_corpus, corpus, 2, 11, 1)
x = range(2, 11, 1)
plt.plot(x, cv)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()

# set the number of clusters in num_topics:
num_topics = 5
lda = models.LdaModel(tfidf_corpus, id2word=dictionary, num_topics=num_topics, random_state = 42)
lda.show_topics(num_topics,num_words=25,formatted=False)
print('\nPerplexity:', lda.log_perplexity(tfidf_corpus))

# Final results - Find the topic number with highest percentage contribution for each article
scores = []
for i in tfidf_corpus:
    scores.append(lda[i])

df['cluster_scores'] = scores

topics = []
for i, row in enumerate(combine['cluster_scores']):
    row = sorted(row, key=lambda x: (x[1]), reverse=True)
    for j, (topic_num, prop_topic) in enumerate(row):
        if j == 0:
            topics.append(int(topic_num))

main_idea = lda.print_topics(num_words=10)
for t in main_idea:
    print(t)

# Sparse + Cosine Similarity
#def get_cosine_sim_sparse(strs):
#    vec = CountVectorizer(token_pattern = "[a-z]{3,}")
#    sparse_matrix = vec.fit_transform(strs)
#    df = pd.DataFrame(sparse_matrix.toarray(), columns = vec.get_feature_names())
#    return (cosine_similarity(df, df))
#
#cosine_sparse = get_cosine_sim_sparse(lemma)

df['final_cluster'] = topics
print(df.groupby('final_cluster').count()) # How many articles in each cluster

pickle.dump( combine, open( "file-clusters.p", "wb" ))
