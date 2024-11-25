# WhiteHatSEO Analyser

This project is a web application built with Flask that analyzes website elements for SEO (Search Engine Optimization), so if you need to compare your website with your competitors check out this project. It provides multiple endpoints that can be accessed via Postman or curl for analyzing and retrieving SEO-related data. 

Using this application you can gain useful SEO suggestions to improve website ranking.

## Table of Contents

1. [Project structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)

## Project structure
```
WhiteHatSEO/
├── app_logic/
│   ├── __init__.py     
│   ├── keywords_logic.py                       # Contains text processing logic
│   ├── methods.py                              # API query routing functions
│   └── values.py                               # Contains Polish stopwords
├── web_crawler/ 
│   ├── __init__.py     
│   └── data_crawler.py                         # Contains a class that extract data from pages
├── web_evaluator/ 
│   ├── __init__.py     
│   ├── data_evaluator_extended.py              # Expanded set of methods responsible for data evaluation (in progress)
│   ├── data_evaluator.py                       # A set of methods that are responsible for assessing data
│   └── website_loading_time_evaluator.py       # A set of methods responsible for assessing the loading time of a website and whether all files have been loaded
├── README.md                                   # Project documentation 
├── requirements.txt                            # Python dependencies
├── app.py                                      # Main application file (Flask app)
└── .gitignore                                  # Git ignore file
```

## Installation

1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/Lewyyy00/WhiteHat-SEO-Analyser.git
    cd WhiteHat-SEO-Analyser
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the Flask server:
    ```bash
    flask run
    ```

5. The application should now be running at `http://127.0.0.1:5000/`.

## Usage

You can use Postman or curl to interact with the WhiteHatSEO Analyser endpoints.

### Postman

1. Open Postman and create a new request.
2. Choose the HTTP method (POST).
3. Input the URL (e.g., `http://127.0.0.1:5000/all`).
4. Send the request and view the response.

### curl

```bash
curl -X POST http://localhost:5000/choose ^
-H "Content-Type: application/json" ^
-d "{\"url\": \"https://example.com\", \"option\": \"content\", \"keywords\": \"example keyword\"}"
```

## API Endpoints

More descriptive and detailed ways to use these endpoints can be found in the app.py file

| Endpoint       | Method | Description                       | Parameters   |
|----------------|--------|-----------------------------------|--------------|
| `/all`     | POST   | Quick, almost complete analysis of website elements | `url`, `keywords`|
| `/choose`  | POST   | A more specific way to extract/analyze just one element                | `url`, `option`, `keywords` |
| `/links` | POST | A set of different options, which extracts links from your page  | `url`, `option` |
| `/keywords`     | POST   | A tool that can compare keywords on your website with those you gave | `url`, `option`, `analysingobject`, `querytext`, `n` |
| `/time`  | POST   | Everything connected with page loading time               | `url`, `option` |
| `/duplicates` | POST | This endpoint can detect how similar are given elements for example contents from pages| `url`, `option`, `links`, `threshold` |
