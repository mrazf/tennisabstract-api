from flask import Flask, jsonify, request, abort
from flask.ext.cors import CORS
import os
import sys
import json
import redis
import logging


app = application = Flask(__name__)
handler = logging.FileHandler('./log.txt')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
cache = redis.StrictRedis(os.environ['TENNIS_ABSTRACT_REDIS_HOST'], port=6379)
CORS(app, origins=['http://localhost:4200', 'http://stringerer.s3-website-eu-west-1.amazonaws.com'])

from tennisabstract_api.name_mappings import name_mappings_api
from tennisabstract_api.players import players_api
app.register_blueprint(name_mappings_api)
app.register_blueprint(players_api)


@app.route("/")
def health():
    return "I am alive"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
