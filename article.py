"""
This is the article module and supports all the ReST actions for the
ARTICLE collection
"""

from datetime import datetime
from flask import make_response, abort
from Modules.crawler.manager import Manager

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


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
    # Create the list of article from our data
    manager = Manager()
    manager.launch_spider()
    return make_response( "LDA model successfully created", 201)
