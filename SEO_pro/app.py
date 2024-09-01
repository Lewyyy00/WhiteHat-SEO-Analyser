from flask import Flask, render_template, jsonify, request
from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from methods import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    query = request.form.get('query')
    analyze_option = request.form.get('analyze_option')
    selected_links = request.form.getlist('selected_links[]')
    
    # Tutaj można dodać logikę analizy SEO na podstawie dostarczonych danych
    response = {
        'url': url,
        'query': query,
        'analyze_option': analyze_option,
        'selected_links': selected_links,
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
