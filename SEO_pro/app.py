from flask import Flask, render_template, jsonify, request
from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from methods import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        link = UrlStructure(url)
        #keyword = request.form.get('keyword')
        internal_links = link.get_all_internal_links()
        return render_template('links.html', links=internal_links, url=url)
    return render_template('index.html')

@app.route('/fetch_meta', methods=['POST'])
def fetch_meta():
    data = request.json
    url = data['url']
    option = data['option']
    meta_data = make_right_choice(url, option)
    if 'error' in meta_data:
        return jsonify(meta_data)

    table_html = '<table>'
    table_html += '<tr><th>Field</th><th>Value</th></tr>'
    
    for key, value in meta_data.items():
        table_html += f'<tr><td>{key}</td><td>{", ".join(map(str, value))}</td></tr>'

    table_html += '</table>'
    return jsonify({'html': table_html})

if __name__ == '__main__':
    app.run(debug=True)