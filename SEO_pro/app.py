from flask import Flask, render_template, jsonify, request
from WhiteHatSEO.SEO_pro.KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from DataAnalyser import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/')
def index():
    page_analyser = UrlStructure('https://wazdan.com')  
    links_200 = page_analyser.get_all_internal_links()
    main_table_data = [{"id": idx + 1, "url": url, "rating": 5} for idx, url in enumerate(links_200)]
    return render_template('index.html', main_table_data=main_table_data)

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