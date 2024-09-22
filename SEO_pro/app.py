from flask import Flask, jsonify, request
from methods import *

app = Flask(__name__)


def validate_params(data, required_params):

    """Check if all required parameters are present."""

    missing_params = [param for param in required_params if not data.get(param)]
    if missing_params:
        return jsonify({"error": f"Missing parameters: {', '.join(missing_params)}"}), 400
    return None

#implement this function into code next time
def process_request(required_params):

    """Helper function to process request and validate params."""

    data = request.json
    validation_error = validate_params(data, required_params)
    if validation_error:
        return validation_error, None
    return None, data

@app.route('/choose', methods=['POST'])
def make_choice():

    """Endpoint for make_right_choice()"""

    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error
    
    result = make_right_choice(data['url'], data['option'], data.get('keywords'))
    return jsonify(result)

@app.route('/links', methods=['POST'])
def links():

    """Endpoint for links_choice()"""
    
    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error
    
    result = links_choice(data['url'], data['option'])
    return jsonify(result)

@app.route('/keywords', methods=['POST'])
def keywords():

    """Endpoint for keyword_options()"""
    
    validation_error, data = process_request(['url', 'option', 'analysingobject'])
    if validation_error:
        return validation_error
    
    result = keyword_options(
        data['url'], 
        data['option'], 
        data['analysingobject'], 
        data.get('querytext'), 
        data.get('n')
    )
    return jsonify(result)

@app.route('/time', methods=['POST'])
def timer():

    """Endpoint for other_options()"""

    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error
    
    result = other_options(data['url'], data['option'])
    return jsonify(result)

@app.route('/duplicates', methods=['POST'])
def duplicates_checker():

    """Endpoint for check_duplicates()"""

    validation_error, data = process_request(['url', 'method'])
    if validation_error:
        return validation_error
    
    result = check_duplicates(data['url'], data['method'], data.get('links'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)