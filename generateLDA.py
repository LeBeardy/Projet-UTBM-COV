"""
This is the article module and supports all the ReST actions for the
generateLDA creation
"""
from flask import make_response, abort
from Modules.LDA.generateLDA import GenerateLDA

def generate():
    """
    This function responds to a request for /api/generateLDA
    with the creation of the LDA Model
    :return:      201 on success
    """
    # Create the list of article from our data
    generator = GenerateLDA()
    generator.generateLDA()
    return make_response( "LDA model successfully created", 201)
