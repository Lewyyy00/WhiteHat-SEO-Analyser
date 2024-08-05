from flask import Flask, render_template, jsonify, request
from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from DataAnalyser import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        keyword = request.form['keyword']
        return render_template('enter_page.html', url=url, keyword=keyword, show_options=True)
    return render_template('enter_page.html', show_options=False)

@app.route('/results', methods=['POST'])
def results():
    url = request.form.get('url')
    keyword = request.form.get('keyword')
    if url:
        page_analyser = UrlStructure(url)
        links_200 = page_analyser.get_all_internal_links()
        main_table_data = [{"id": idx + 1, "url": url, "rating": 5} for idx, url in enumerate(links_200)]
        return render_template('results.html', main_table_data=main_table_data)
    else:
        return "No URL provided", 400

@app.route('/details/<int:id>/<string:detail_type>')
def details(id, detail_type):
    if detail_type == "title":
        title_analyzer = TitleAnalyzer()
        title_data = title_analyzer.analyze_titles()
        details = title_data[id - 1] if id <= len(title_data) else {}
    else:
        details_table_data = {
            "meta_description": {
                1: [{"detail_id": 1, "info": "Meta Description 1 for URL 1"}, {"detail_id": 2, "info": "Meta Description 2 for URL 1"}],
                2: [{"detail_id": 3, "info": "Meta Description 1 for URL 2"}],
                3: [{"detail_id": 4, "info": "Meta Description 1 for URL 3"}, {"detail_id": 5, "info": "Meta Description 2 for URL 3"}],
            },
            "headings": {
                1: [{"detail_id": 1, "info": "Heading 1 for URL 1"}, {"detail_id": 2, "info": "Heading 2 for URL 1"}],
                2: [{"detail_id": 3, "info": "Heading 1 for URL 2"}],
                3: [{"detail_id": 4, "info": "Heading 1 for URL 3"}, {"detail_id": 5, "info": "Heading 2 for URL 3"}],
            }
        }
        details = details_table_data.get(detail_type, {}).get(id, [])
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True)