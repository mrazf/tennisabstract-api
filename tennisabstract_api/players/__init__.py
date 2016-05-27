from flask import Blueprint, jsonify, abort
from tennisabstract_api import cache

players_api = Blueprint('players_api', __name__)

@players_api.route("/api/players/<name>", methods = ['GET'])
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
