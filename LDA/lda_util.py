import os
import pandas as pd
import numpy as np
import datetime as dt
import time

%load_ext ipycache

import random
import re
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import json

articles = []

prepared_articles = []

for article in articles :
    prepared_articles.append(article.get("text"))
