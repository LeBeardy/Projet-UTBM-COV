# Import libraries
import sqlite3
import pickle
import yaml
import os

from gensim import corpora, utils, models, similarities
from collections import defaultdict

# Import modules
from Modules.data.manager import Manager

class GenerateLDA:

    def __init__(self):
        project_folder = os.getcwd()
        # Load configuration
        with open(project_folder + '/config.yml') as fp:
            config = yaml.load(fp, Loader = yaml.FullLoader)
        fp.close()

        # Basic passes
        self.NUM_PASSES = 10
        self.NUM_TOPICS = 100
        self.RANDOM_STATE = 1

        # Database and other resources
        self.DATABASE_PATH = config['paths']['database']
        self.LDA_PATH = config['paths']['lda']
        self.DICTIONARY_PATH = config['paths']['dictionary']
        self.CORPUS_PATH = config['paths']['corpus']


    def generateLDA(self):
        # Execution
        manager = Manager(self.DATABASE_PATH)
        dictionary = corpora.Dictionary(manager)
        # Remove words that appear less than 5 times and that are in more than in 80% documents
        dictionary.filter_extremes(no_below=5, no_above=0.8)
        corpus = [dictionary.doc2bow(text) for text in manager]

        # LDA Model
        lda = models.LdaModel(corpus, id2word=dictionary, random_state=self.RANDOM_STATE,
                              num_topics=self.NUM_TOPICS, passes=self.NUM_PASSES)

        # Save resources
        lda.save(self.LDA_PATH)
        with open(self.DICTIONARY_PATH, 'wb') as fp:
            pickle.dump(dictionary, fp)
        fp.close()
        with open(self.CORPUS_PATH, 'wb') as fp:
            pickle.dump(corpus, fp)
        fp.close()
