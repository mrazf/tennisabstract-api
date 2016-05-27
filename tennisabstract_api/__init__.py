from flask import Flask, jsonify, request, abort
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import sys
import json
import redis
import logging


def setup_driver():
    driver = None
    try:
        driver = webdriver.PhantomJS('poop', service_log_path=os.path.devnull)
    except WebDriverException as e:
        app.logger.error(e)
    except Exception as e:
        app.logger.error(e)

    return driver

app = application = Flask(__name__)
handler = logging.FileHandler('./log.txt')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
driver = setup_driver()
cache = redis.StrictRedis(os.environ['TENNIS_ABSTRACT_REDIS_HOST'], port=6379)

from tennisabstract_api.name_mappings import name_mappings_api
from tennisabstract_api.players import players_api
app.register_blueprint(name_mappings_api)
app.register_blueprint(players_api)


@app.route("/")
def health():
    return "I am alive"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
