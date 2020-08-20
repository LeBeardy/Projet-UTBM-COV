"""
This is the article module and supports all the ReST actions for the
generateLDA creation
"""
from flask import make_response, abort
from Modules.LDA.generateLDA import GenerateLDA
from flask import Flask , render_template, jsonify, request, redirect, url_for
def generate():
    """
    This function responds to a request for /api/generateLDA
    with the creation of the LDA Model
    :return:      201 on success
    """
    # Create the list of article from our data
    generator = GenerateLDA()
    generator.generateLDA()
    return jsonify({"code": 200, "message" : "LDA model successfully created."})
