from flask import Flask, render_template, jsonify, request
from logic import *
from analyser import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/')
def index():
    page_analyser = UrlStructure('https://wazdan.com')  # Zmień na odpowiednią stronę
    links_200 = page_analyser.get_all_internal_links()
    main_table_data = [{"id": idx + 1, "url": url, "rating": 5} for idx, url in enumerate(links_200)]
    return render_template('index.html', main_table_data=main_table_data)

@app.route('/details/<int:id>')
def details(id):
    details_table_data = {
        1: [{"detail_id": 1, "info": "Detail 1 for URL 1"}, {"detail_id": 2, "info": "Detail 2 for URL 1"}],
        2: [{"detail_id": 3, "info": "Detail 1 for URL 2"}],
        3: [{"detail_id": 4, "info": "Detail 1 for URL 3"}, {"detail_id": 5, "info": "Detail 2 for URL 3"}],
    }
    details = details_table_data.get(id, [])
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True)