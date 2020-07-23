import os
import pandas as pd
import numpy as np
import datetime as dt
import time
import ndjson

import random
import re
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import json

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:99% !important; }</style>"))

project_folder = os.getcwd()

books = []
t=""
with open(project_folder+'/data/books.ndjson', 'r') as fin:
    books = [json.loads(l) for l in fin]

books_with_wikipedia = [book for book in books if 'Wikipedia:' in book[0]]
print(f'Found with wikipedia a total of {len(books_with_wikipedia)} books.')
books = [book for book in books if 'Wikipedia:' not in book[0]]
print(f'Found a total of {len(books)} books.')


from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(articles_model)
from itertools import islice
def take(n, iterable):
    return list(islice(iterable, n))

items_5 = take(5, dictionary.iteritems())
print(items_5)
bow_corpus = [dictionary.doc2bow(text) for text in articles_model]
print('Number of unique tokens: %d' % len(dictionary)) # roughly 400 less than in presentation
print('Number of articles: %d' % len(bow_corpus)) # roughly 500 less than in presentation
print(bow_corpus[0])
