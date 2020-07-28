"""
This is the article module and supports all the ReST actions for the
ARTICLE collection
"""

from datetime import datetime
from flask import make_response, abort
from Modules.crawler.manager import Manager
from articleCrawler.articleCrawler.spiders.getpmids_spider import ArticlesSpider
import crochet
crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time


output_data = []
crawl_runner = CrawlerRunner()

def read_all():
    """
    This function responds to a request for /api/article
    with the complete lists of article
    :return:        json string of list of article
    """
    # Create the list of article from our data
    return [ARTICLE[key] for key in sorted(ARTICLE.keys())]


def read_one(id):
    """
    This function responds to a request for /api/article/{id}
    with one matching article from article
    :param id:   id of article to find
    :return:        article matching last name
    """
    # Does the article exist in article?
    if id in ARTICLE:
        article = ARTICLE.get(id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Article with last name {id} not found".format(id=id)
        )

    return article


def generate():
    """
    This function responds to a request for /api/article/generate
        with the fetch of the articles
    :return:      201 on success
    """
    scrape_with_crochet()

    return jsonify(output_data)


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet():
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
