# WhiteHatSEO Analyser

This project is a web application built with Flask that analyzes website elements for SEO (Search Engine Optimization). It provides multiple endpoints that can be accessed via Postman or curl for analyzing and retrieving SEO-related data. 

Using this application you can gain useful SEO suggestions to improve website ranking.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Examples](#examples)
5. [License](#license)

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