#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:37:55 2020

@author: lynnjiang
"""

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import json
import pandas as pd
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer



with open('bostonglobe2014_2.json') as f:
        #f = open('bostonglobe2014_2.json')
        data = json.load(f)

for i in range(len(data)):
    data[i] = str(data[i]).replace('[','').replace(']','')
    

data_df = pd.DataFrame(data)
data_df_0 = pd.DataFrame(data)

def remove_stopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words


def word_lemmatizer(text):
    lem_text = [WordNetLemmatizer.lemmatize(i) for i in text]
    return lem_text


def word_stemmer(text):
    stem_text = [PorterStemmer.stem(i) for i in text]
    return stem_text
                    

#tokenizer = RegexpTokenizer(r'\\w+')
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
data_df[0] = data_df[0].apply(lambda x: tokenizer.tokenize(str(x).lower()))


#data_df_1 = data_df[0].apply(lambda x: remove_stopwords(x))


#vectorizer = TfidfVectorizer()
#response = vectorizer.fit_transform(data_df_1[0])
#feature_names = vectorizer.get_feature_names()
#dense = response.todense()
#denselist = dense.tolist()
#token_df = pd.DataFrame(denselist, columns=feature_names)
#data_df.reset_index(drop=True, inplace=True)
#token_df.reset_index(drop=True, inplace=True)
#data_df_2 = pd.concat([data_df_0[0], token_df], axis=1)



print(data_df_0)








































