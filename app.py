from flask import Flask, jsonify, request
from methods import *

app = Flask(__name__)


def validate_params(data, required_params):

    """Check if all required parameters are present."""

    missing_params = [param for param in required_params if not data.get(param)]
    if missing_params:
        return jsonify({"error": f"Missing parameters: {', '.join(missing_params)}"}), 400
    return None

def process_request(required_params):

    """Helper function to process request and validate params."""

    data = request.json
    validation_error = validate_params(data, required_params)
    if validation_error:
        return validation_error, None
    return None, data

@app.route('/choose', methods=['POST'])
def make_choice():

    """
    Endpoint for make_right_choice()

    Accepted options:
        - 'title'
        - 'metadescription'
        - 'headings'
        - 'content'
        - 'altcontent'
        - 'urlcontent'

    You can also provide a 'keywords' field for content-related options.

    Example request body:
    {
        "url": "https://example.com",
        "option": "title",
        "keywords": "example keyword"
    }

    """
    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error

    result = make_right_choice(data['url'], data['option'], data.get('keywords'))

    if data['option'] in ['content', 'altcontent']:
        if not data.get('keywords'): 
            return jsonify({'error': 'The option "content" or "altcontent" requires keywords.'}), 400

    print(data)
    return jsonify(result)

@app.route('/links', methods=['POST'])
def links():

    """
    Endpoint for links_choice()

    Accepted options:
        - 'valid' - All links with status 200
        - 'notvalid' - All links with a status other than 200
        - 'domain' - All domain links
        - 'canonical' - All canonical links from domain links
        - 'external' - All links other than domain links
        - 'status' - All domain links with statuses 

    Example request body:
    {
        "url": "https://example.com",
        "option": "status"
    }
    
    """
    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error
    
    result = links_choice(data['url'], data['option'])
    return jsonify(result)

@app.route('/keywords', methods=['POST'])
def keywords():

    """
    Endpoint for keyword_options()
    
    Accepted options:
        - 'mostpopularngrams' - Most popular Ngrams in the analysing object
        - 'ngramsinquery' - Most popular Ngrams in the query (keywords)
        - 'contentwithkeywords' - Shows which keywords are in the analysing object  
        - 'keywordsdensity' - Shows keywords density so Shows keywords density so (the amount of keywords in a analyzing object/the amount of words in a analyzing object)
        - 'all' - Each option from the top

    Accepted analysingobject:
        - 'title'
        - 'metadescription'
        - 'headings' 
        - 'content' 
        - 'altcontent' 
        - 'urlcontent'

    You can also provide a 'querytext' and 'n' fields. Querytext is just the query you would use 
    in a browser or you can treat it as a set of keywords. 'n' is a size of ngram.

    Example request body:
    {
        "url": "https://example.com",
        "option": "all",
        "analysingobject": "title",
        "querytext": "one example ",
        "n": "2"
    }

    """
    validation_error, data = process_request(['url', 'option', 'analysingobject'])
    if validation_error:
        return validation_error
    
    print(data)
    
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

    """Endpoint for other_options()

    Accepted options:
        - 'websitetimeload' - returns the time at which the page loaded
        - 'filecorrectness' - checks if all files loaded in the webiste #does not work 

    Example request body:
    {
        "url": "https://example.com",
        "option": "websitetimeload",
    }

    """

    validation_error, data = process_request(['url', 'option'])
    if validation_error:
        return validation_error
    
    result = time_options(data['url'], data['option'])
    return jsonify(result)

@app.route('/duplicates', methods=['POST'])
def duplicates_checker():

    """
    Endpoint for check_duplicates()

    Accepted methods:
        - 'title' - returns the time at which the page loaded
        - 'meta' - checks if all files loaded in the webiste #does not work 
        - 'content' - checks if all files loaded in the webiste #does not work 

    Example request body:
    {
        "url": "https://example.com",
        "option": "websitetimeload",
        "links": ["https://example.com", "https://example2.com", "https://example3.com"],
        "threshold": "0.8"
    }6

    """

    validation_error, data = process_request(['url', 'method'])
    if validation_error:
        return validation_error
    
    result = check_duplicates(data['url'], data['method'], data.get('links'), data.get('threshold'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)