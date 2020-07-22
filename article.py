"""
This is the article module and supports all the ReST actions for the
ARTICLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
ARTICLE = {
    1: {
        "id":1,
        "title": "Doug",
        "text": "Farrell",
        "timestamp": get_timestamp(),
    },
    2: {
        "id":2,
        "title": "Kent",
        "text": "Brockman",
        "timestamp": get_timestamp(),
    },
    3: {
        "id":3,
        "title": "Bunny",
        "text": "Easter",
        "timestamp": get_timestamp(),
    },
}


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


def create(article):
    """
    This function creates a new article in the article structure
    based on the passed in article data
    :param article:  article to create in article structure
    :return:        201 on success, 406 on article exists
    """
    text = article.get("text", None)
    title = article.get("title", None)
    id = article.get("id", None)
    # Does the article exist already?
    if id not in ARTICLE and id is not None:
        ARTICLE[id] = {
            "id": id,
            "text": text,
            "title": title,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{id} successfully created".format(id=id), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Article with last name {id} already exists".format(id=id),
        )


def update(id, article):
    """
    This function updates an existing article in the article structure
    :param id:  id of article to update in the article structure
    :param article:  article to update
    :return:        updated article structure
    """
    # Does the article exist in article?
    if id in ARTICLE:
        ARTICLE[id]["title"] = article.get("title")
        ARTICLE[id]["text"] = article.get("text")
        ARTICLE[id]["timestamp"] = get_timestamp()

        return ARTICLE[id]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Article with last name {id} not found".format(id=id)
        )


def delete(id):
    """
    This function deletes a article from the article structure
    :param id:   id of article to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the article to delete exist?
    if id in ARTICLE:
        del ARTICLE[id]
        return make_response(
            "article {id} successfully deleted".format(id=id), 200
        )

    # Otherwise, nope, article to delete not found
    else:
        abort(
            404, "Article with id {id} not found".format(id=id)
        )
