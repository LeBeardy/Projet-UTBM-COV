"""
This is the dla_article module and supports all the ReST actions for the
DLA_ARTICLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
DLA_ARTICLE = {
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
    This function responds to a request for /api/dla_article
    with the complete lists of dla_article
    :return:        json string of list of dla_article
    """
    # Create the list of dla_article from our data
    return [DLA_ARTICLE[key] for key in sorted(DLA_ARTICLE.keys())]


def read_one(id):
    """
    This function responds to a request for /api/dla_article/{id}
    with one matching dla_article from dla_article
    :param id:   id of dla_article to find
    :return:        dla_article matching last name
    """
    # Does the dla_article exist in dla_article?
    if id in DLA_ARTICLE:
        dla_article = DLA_ARTICLE.get(id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Dla_article with last name {id} not found".format(id=id)
        )

    return dla_article


def create(dla_article):
    """
    This function creates a new dla_article in the dla_article structure
    based on the passed in dla_article data
    :param dla_article:  dla_article to create in dla_article structure
    :return:        201 on success, 406 on dla_article exists
    """
    text = dla_article.get("text", None)
    title = dla_article.get("title", None)
    id = dla_article.get("id", None)
    # Does the dla_article exist already?
    if id not in DLA_ARTICLE and id is not None:
        DLA_ARTICLE[id] = {
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
            "Dla_article with last name {id} already exists".format(id=id),
        )


def update(id, dla_article):
    """
    This function updates an existing dla_article in the dla_article structure
    :param id:  id of dla_article to update in the dla_article structure
    :param dla_article:  dla_article to update
    :return:        updated dla_article structure
    """
    # Does the dla_article exist in dla_article?
    if id in DLA_ARTICLE:
        DLA_ARTICLE[id]["title"] = dla_article.get("title")
        DLA_ARTICLE[id]["text"] = dla_article.get("text")
        DLA_ARTICLE[id]["timestamp"] = get_timestamp()

        return DLA_ARTICLE[id]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Dla_article with last name {id} not found".format(id=id)
        )


def delete(id):
    """
    This function deletes a dla_article from the dla_article structure
    :param id:   id of dla_article to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the dla_article to delete exist?
    if id in DLA_ARTICLE:
        del DLA_ARTICLE[id]
        return make_response(
            "dla_article {id} successfully deleted".format(id=id), 200
        )

    # Otherwise, nope, dla_article to delete not found
    else:
        abort(
            404, "Dla_article with id {id} not found".format(id=id)
        )
