from flask import Flask, render_template, jsonify, request
from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from DataAnalyser import *
from methods import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        link = UrlStructure(url)
        #keyword = request.form.get('keyword')
        internal_links = link.get_all_internal_links()
        return render_template('mainpage.html', links=internal_links, url=url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)