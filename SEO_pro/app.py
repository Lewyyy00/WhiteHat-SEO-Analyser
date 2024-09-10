from flask import Flask, jsonify, request
from methods import *

app = Flask(__name__)


def validate_params(data, option, keywords):

    """checks if the user has given the correct option or data"""

    if not data or not option:
        return jsonify({"error": "Invalid parameters"}), 400

@app.route('/choose', methods=['POST'])
def make_choice():

    """endpoint for make_right_choice()"""

    data = request.json
    url = data.get('url')
    option = data.get('option')
    keywords = data.get('keywords', None)

    validate_params(data, option, keywords)

    result = make_right_choice(url, option, keywords)
    return jsonify(result)

@app.route('/links', methods=['POST'])
def links():

    """endpoint for links_choice()"""

    data = request.json
    url = data.get('url')
    option = data.get('option')

    validate_params(data, option, None)

    result = links_choice(url, option)
    return jsonify(result)

@app.route('/keywords', methods=['POST'])
def keywords():

    """endpoint for keyword_options()"""

    data = request.json
    url = data.get('url')
    option = data.get('option')
    text = data.get('text')
    querytext = data.get('querytext', None)
    n = data.get('n', None)

    validate_params(data, option, None)

    result = keyword_options(url, option, text, querytext, n)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)