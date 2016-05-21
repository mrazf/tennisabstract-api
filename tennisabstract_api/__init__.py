from flask import Flask, jsonify
from selenium import webdriver
import redis

app = application = Flask(__name__)
cache = redis.StrictRedis(host='tennisabstract-cache.9lg61v.0001.euw1.cache.amazonaws.com', port=6379)
driver = webdriver.PhantomJS('./node_modules/phantomjs/bin/phantomjs')

@app.route("/api/player/<name>")
def player(name):
    result = get_from_cache(name)
    print result
    if result: return result

    driver.get("http://www.tennisabstract.com/cgi-bin/player.cgi?p=" + name)
    biography = driver.find_element_by_id("biog")
    player_name = biography.find_element_by_xpath("./table/tbody/tr[1]/td/span").text
    player_dob = biography.find_element_by_xpath("./table/tbody/tr[2]/td").text

    result = jsonify({
        "name": player_name,
        "dateOfBirth": player_dob
    })
    store_in_cache(name, result)

    return result


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
