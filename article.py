"""
This is the article module and supports all the ReST actions for the
ARTICLE collection
"""

from datetime import datetime
from flask import make_response, abort
from Modules.data.manager import Manager
from Modules.LDA.Evaluator import Evaluator
from articleCrawler.articleCrawler.spiders.getpmids_spider import ArticlesSpider
import crochet
crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
import os
import generateLDA
output_data = []
crawl_runner = CrawlerRunner()

def read_all():
    """
    This function responds to a request for /api/article
    with the complete lists of article
    :return:        json string of list of article
    """
    database_manager = Manager(os.getcwd() + "/data/database/data.db")
    return jsonify(database_manager.get_articles())


def read_one(pmid):
    """
    This function responds to a request for /api/article/{pmid}
    with one matching article from article
    :param pmid:   pmid of article to find
    :return:        article matching pmid
    """
    database_manager = Manager(os.getcwd() + "/data/database/data.db")
    evaluator = Evaluator()
    article = database_manager.get_article(pmid)
    #find the recommendations for the article, it take the full article, if it got one, else the abstract
    content = article["content_full"] if article["content_full"] !='' else article["content_abstract"]
    article["recommendation"] = evaluator.get_recommendations(content)
    return jsonify(article)


def generate():
    """
    This function responds to a request for /api/article/generate
        with the fetch of the articles
    :return:      201 on success
    """
    scrape_with_crochet()
    generateLDA.generate()
    return jsonify(output_data)


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet():
    """
    Function who permit to call the crawler to fetch the articles.
    The crawler is launched in an asynchronous processus.
    """
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl( ArticlesSpider)
    return eventual  # returns a twisted.internet.defer.Deferred

def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    output_data.append(dict(item))

def recommendations(pmid):
    """
    This function responds to a request for /api/recommendations/{pmid}
    with the recommendations of article for a specific one
    :param pmid:   pmid of the article you want to get the recommendations from
    :return:        list of recommendations
    """
    database_manager = Manager(os.getcwd() + "/data/database/data.db")
    evaluator = Evaluator()
    article = database_manager.get_article(pmid)
    content = article["content_full"] if article["content_full"] !='' else article["content_abstract"]
    recommendations = evaluator.get_recommendations(content)

    return jsonify(recommendations)
