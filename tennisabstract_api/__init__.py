from flask import Flask, jsonify
from selenium import webdriver

app = application = Flask(__name__)
driver = webdriver.PhantomJS('./node_modules/phantomjs/bin/phantomjs')

@app.route("/api/player/<name>")
def player(name):
    driver.get("http://www.tennisabstract.com/cgi-bin/player.cgi?p=" + name)
    biography = driver.find_element_by_id("biog")
    player_name = biography.find_element_by_xpath("./table/tbody/tr[1]/td/span").text
    player_dob = biography.find_element_by_xpath("./table/tbody/tr[2]/td").text

    return jsonify({
            "name": player_name,
            "dateOfBirth": player_dob
        })

@app.after_request
def add_header(response):
    response.cache_control.max_age = 21600

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
