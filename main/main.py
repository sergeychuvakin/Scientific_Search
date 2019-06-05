#!/usr/bin/env python
# coding: utf-8

# In[3]:


import re
import time
from bs4 import BeautifulSoup
import requests
import json
#import Levenshtein as lv
import numpy as np
from gensim import corpora, models, similarities
import spacy

import pandas as pd
#for findDOI
import feedparser
import jellyfish
import copy


# In[1]:


from rss import rss # список рассылки
from findDOI import findDOI # функция поиска doi по названию
from ALT import altmetrics # функция поиска альтметрик 
from stoplist import stoplist #стоп-лист
from rssParser import Parser # класс, который парсит рсс, в датафрейм, - предлагаю его использовать для наполненния
from findJournal import findJournal # функция поиска названия журнала по названию статьи


# In[4]:


# p = Parser(rss)
# df = p.main()
#df.to_csv('example_table.csv')
df = pd.read_csv('example_table.csv')


# In[5]:


findJournal(df.loc[1,]["article_name"])


# In[6]:


nlp = spacy.load('en', parser=False, ner=False)  


# In[ ]:




