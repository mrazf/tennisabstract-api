from flask import Flask, jsonify, request, abort
from selenium import webdriver
import os
import json
import redis

app = application = Flask(__name__)
cache = redis.StrictRedis(os.environ['TENNIS_ABSTRACT_REDIS_HOST'], port=6379)
driver = webdriver.PhantomJS(os.environ['TENNIS_ABSTRACT_PHANTOM_PATH'], service_log_path=os.path.devnull)

from tennisabstract_api.name_mappings import api
app.register_blueprint(api)

@app.route("/")
def health():
    return "I am alive"


@app.route("/api/players/<name>", methods = ['GET'])
def player(name):
    tennisAbstractName = get_from_cache('nameMapping' + name)
    result = get_from_cache(tennisAbstractName)

    if result:
        return jsonify(json.loads(result))

    tennisAbstractName = get_from_cache('nameMapping' + name)
    driver.get("http://www.tennisabstract.com/cgi-bin/player.cgi?p=" + tennisAbstractName)
    biography = driver.find_element_by_id("biog")
    player_name = biography.find_element_by_xpath("./table/tbody/tr[1]/td/span").text
    player_dob = biography.find_element_by_xpath("./table/tbody/tr[2]/td").text

    result = {
        "name": player_name,
        "dateOfBirth": player_dob
    }
    store_in_cache(tennisAbstractName, json.dumps(result))

    return jsonify(result)


def get_from_cache(name):
    return cache.get(name)


def store_in_cache(key, val):
    cache.set(key, val)


@app.after_request
def add_header(response):
    response.cache_control.max_age = 21600

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
