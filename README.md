# WhiteHatSEO Analyser

This project is a web application built with Flask that analyzes website elements for SEO (Search Engine Optimization). It provides multiple endpoints that can be accessed via Postman or curl for analyzing and retrieving SEO-related data. 

Using this application you can gain useful SEO suggestions to improve website ranking.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [License](#license)

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

## License
MIT License

Copyright (c) 2024 Michał Lewandowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.