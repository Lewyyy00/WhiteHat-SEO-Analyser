from flask import Flask, render_template, request, redirect, url_for
from logic import WebsiteData

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result_page', methods=['POST'])
def submit():
    url = request.form['url']
    keywords = request.form['keywords']
    website_data = WebsiteData(url)

    title = website_data.get_title()
    headings = website_data.get_headings()
    paragraphs = website_data.get_paragraphs()
    all_links = website_data.get_all_links()
    all_404 = website_data.get_all_404_links()

    return render_template('results.html', 
                           title = title, 
                           headings = headings, 
                           paragraphs = paragraphs, 
                           all_links = all_links,
                           all_404 = all_404)

if __name__ == '__main__':
    app.run(debug=True)