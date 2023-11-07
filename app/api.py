import os
from flask import Blueprint, jsonify, request, json
from webapp.behavior_trees.espresso_automat import *


# REST-Api
api_blueprint = Blueprint("api", __name__)

################################################################################################################
# GENERAL
################################################################################################################


@api_blueprint.route("info/", methods=["GET"])
def get_api_info():
    """
    Return information about the api and the server.
    """
    res = {"SMART_HOME": "api", "version": "1.0"}
    return jsonify(res)


################################################################################################################
# BEHAVIOR TREES
################################################################################################################


@api_blueprint.route("trigger_espresso_automat_tree/", methods=["POST"])
def trigger_espresso_automat_tree():
    """
    Trigger Espresso automat behavior tree.
    """
    # data = request.json
    try:
        program, strength, temperature, quantity = espresso_automat_main()
        status_code = 200
        res = {'program': program,
               'strength': strength,
               'temperature': temperature,
               'quantity': quantity}
    except:
        status_code = 444
        res = {}
    return jsonify(res), status_code
