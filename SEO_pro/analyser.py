import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from logic import *
from values import polish_stopwords
import pandas as pd
from typing import Optional
import json
from collections import Counter
nltk.download('stopwords')
nltk.download('punkt')

class BaseStructure:
    def __init__(self, website: str):
        self.website = website
        self.soup: Optional[BeautifulSoup] = None
        self._initialize_soup()

    def _initialize_soup(self):
        try:
            response = requests.get(self.website)
            response.raise_for_status()  # Raise an error for bad status codes
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as error:
            print(f"Błąd podczas pobierania strony: {error}")
            self.soup = None

def handle_request_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.RequestException as error:
            print(error)
            return None
    return wrapper

#1 URL Structure
class UrlStructure(BaseStructure):
 
    @handle_request_errors
    def get_all_200_links(self):
        if self.soup:
            links = self.soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
            links_200 = []
            
            for link in links:
                href = link['href']
                full_url = urljoin(self.website, href)
                if not urlparse(full_url).scheme:
                    print(f"Invalid URL: {href}")
                    continue
        
                link_response = requests.get(full_url, timeout=1)
                if link_response.status_code == 200:
                    links_200.append(full_url)                 
            return links_200
        return None
    
    @handle_request_errors
    def get_all_not_valid_links(self):
        if self.soup:
            links = self.soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
            error_links = {}  # Słownik do przechowywania błędnych linków i ich statusów
            
            for link in links:
                href = link['href']
                full_url = urljoin(self.website, href)
                if not urlparse(full_url).scheme:
                    print(f"Invalid URL: {href}")
                    continue
                try:
                    link_response = requests.get(full_url, timeout=1)
                    if link_response.status_code != 200:
                        if link_response.status_code not in error_links:
                            error_links[link_response.status_code] = []
                        error_links[link_response.status_code].append(full_url)
                except requests.exceptions.Timeout:
                    print(f"Timeout checking {full_url}")
                    if 'Timeout' not in error_links:
                        error_links['Timeout'] = []
                    error_links['Timeout'].append(full_url)
                except requests.exceptions.RequestException as e:
                    print(f"Error checking {full_url}: {e}")
                    if 'RequestException' not in error_links:
                        error_links['RequestException'] = []
                    error_links['RequestException'].append(full_url)     
            return error_links
        return None
    
    # it doesnt recognise the same website but with other domain in case of changeing langauge (TLD) example.pl != example.com
    def get_all_internal_links(self):
        if self.soup:
            parsed_url = urlparse(self.website)
            url_domain = parsed_url.netloc
            links = self.soup.find_all('a', href=True)
            internal_links = []

            for link in links:
                href = link['href']
                full_url = urljoin(self.website, href)
                potential_internal_link = urlparse(full_url)
                if url_domain == potential_internal_link.netloc:
                    internal_links.append(full_url)
            return internal_links
        return None

    def get_all_external_links(self):
        if self.soup:
            parsed_url = urlparse(self.website)
            url_domain = parsed_url.netloc
            links = self.soup.find_all('a', href=True)
            internal_links = []

            for link in links:
                href = link['href']
                full_url = urljoin(self.website, href)
                potential_internal_link = urlparse(full_url)
                if url_domain != potential_internal_link.netloc:
                    internal_links.append(full_url)
            return internal_links
        return None

class DataFromUrl(BaseStructure):   

    def split_url(self):
        url = re.sub(r'^https?:\/\/', '', self.website)
        url = re.sub(r'[\/\-_?&=]', ' ', url)
        potential_keywords = url.split()
        return potential_keywords

    def find_keywords_url(self):
        keywords_url = self.split_url()
        url_keywords = [keyword for keyword in keywords_url if any(key in keyword for key in self.keywords)]
        return url_keywords

    def get_lenght_url(self):
        url_without_protocol  = re.sub(r'^https?:\/\/', '', self.website)
        lenght = len(url_without_protocol)
        return lenght

    """def get_parsed_url(self):
        parsed_url = urlparse(self.website)
        url_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
        return url_parts"""
    
    def is_url_has_https(self):
        parsed_url = urlparse(self.website)
        data = parsed_url.scheme

        if data == 'https':
            pass
        elif data == 'http':
            pass
        else:
            pass

        pass

    @handle_request_errors
    def get_website_language(self):
        if self.soup:
            html_tag = self.soup.find('html')
            if html_tag.has_attr("lang"):
                return html_tag['lang']
        return None
        
    def get_stopwords_language(self):
        web_lang = self.get_website_language()
        
        if web_lang.startswith('pl'):
            stopwordss = polish_stopwords
        else:
            stopwordss = set(stopwords.words("english"))
        return stopwordss
        
    def find_stopwords(self):
        stop_words = self.get_stopwords_language()
        splited_url = self.split_url()

        list_of_stopwords = [element for element in splited_url if element in stop_words]
        return list_of_stopwords

    def analyze_url_hyphens(self):

        for i in enumerate(self.website):
            if i == '_':
                return print(f'{self.website} has emphasis')
            else:
                return print(f'{self.website} does not have emphasis')

    def find_capital_letters(self):
        for i in self.url:
            if i.isupper():
                return f'{self.website} has capital letters'
        f'{self.url} does not have capital letters'

    def find_any_not_ascii_letters(self):
        non_ascii_chars = [char for char in self.website if ord(char) > 127]
        return non_ascii_chars


    pass

# HTML 
class DataFromHtmlStructure(BaseStructure):
 
    @handle_request_errors
    def get_title(self):
        titles_list = []
        if self.soup:
            title_tag = self.soup.find_all('title')
            for title in title_tag:
                title_text = title.get_text()
                titles_list.append(title_text)
            return titles_list
        return None

    @handle_request_errors    
    def get_headings(self):
        headings_dictionary = {}
        if self.soup:
            headings = self.soup.find_all(['h1','h2','h3','h4','h5','h6'])
            for heading in headings:
                if heading.name not in headings_dictionary:
                    headings_dictionary[heading.name] = []
                headings_dictionary[heading.name].append(heading.get_text())
            return headings_dictionary
        return None
    
    @handle_request_errors    
    def get_all_h1(self):
        headings_dictionary = []
        if self.soup:
            headings = self.soup.find_all('h1')
            for heading in headings:
                heading_name = heading.get_text()
                headings_dictionary.append(heading_name)
            return headings_dictionary
        return None
    
    @handle_request_errors    
    def get_all_h2(self):
        headings_dictionary = []
        if self.soup:
            headings = self.soup.find_all('h2')
            for heading in headings:
                heading_name = heading.get_text()
                headings_dictionary.append(heading_name)
            return headings_dictionary
        return None
    
    @handle_request_errors
    def get_meta_description(self):
        meta_description_list = []
        if self.soup:
            meta_descriptios = self.soup.find_all('meta', attrs={"name": "description"})
            for meta_description in meta_descriptios:
                if 'content' in meta_description.attrs:
                    clean_content = meta_description['content'].replace('\xa0', ' ')
                    meta_description_list.append(clean_content)
                return meta_description_list
            else:
                return None
        return None
     
class TextStructures(BaseStructure):
    
    @handle_request_errors
    def get_content(self):
        if self.soup:
            paragraphs = self.soup.find_all('p')
            return [paragraph.text for paragraph in paragraphs]
        return None
    
    @handle_request_errors
    def get_all_alt_texts(self):
        if self.soup:
            images = self.soup.find_all('img', src = True)
            return [alt_text.get('alt') for alt_text in images]
        return None

class AnalyseData:
    def __init__(self, data):
        self.data = data

    def is_right_file(self):
        if isinstance(self.data, list) or isinstance(self.data, str):
            newdata = {
                "Text": self.data 
            }
            json_data = json.dumps(newdata)
            return json_data
        
        elif isinstance(self.data, dict):  
            rows = []
            for heading, texts in self.data.items():
                for text in texts:
                    rows.append({"Headings": heading, "Text": text})

            json_data = json.dumps(rows)
            return json_data
        else:
            return json.dumps([])
            
    def count_words(self, text):
        words = text.split()
        return len(words)

    def count_words_in_list(self, elements):
        numer_of_words = [self.count_words(element) for element in elements]
        return numer_of_words

#needs to be fixed
    def is_length_alright(self):
        json_data = self.is_right_file()
        data = json.loads(json_data)
        if isinstance(data, dict) and "Text" in data:
            texts = data["Text"]
            lengths = [len(text) for text in texts]
            elements_in_list = [len(texts)]
            word_counts = [self.count_words(text) for text in texts]
            result = {
                "Text": texts,
                "length": lengths,
                "word_count": word_counts,
                "elements": elements_in_list
            }
            return json.dumps(result)
        elif isinstance(data, list):
            for element in data:
                element["length"] = len(element["Text"])
                element["word_count"] = self.count_words(element["Text"])
            return json.dumps(data)
        return json.dumps([])

    def is_missing(self):
        json_data = self.is_length_alright()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Missing value"] = [length == 0 for length in data["length"]]
            data["Missing value"] = ["True" if x else "False" for x in data["Missing value"]]
            return json.dumps(data)
        elif isinstance(data, list):
            for element in data:
                element["Missing value"] = "True" if element["length"] == 0 else "False"
            return json.dumps(data)
        return json.dumps([])

    def is_multiple(self):
        json_data = self.is_missing()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Multiple values"] = [length != 1 for length in data["elements"]]
            data["Multiple values"] = ["True" if x else "False" for x in data["Multiple values"]]
            return json.dumps(data)
        elif isinstance(data, list):
            headings = [d['Headings'] for d in data]
            amount_of_headings = Counter(headings)

            if amount_of_headings.get('h1', 0) == 1:
                for element in data:
                    if element.get('Headings') == 'h1':
                        element["Multiple values"] = "False"
                    elif element.get('Headings') != 'h1':
                        element["Multiple values"] = "does not influance SEO" #change to sth else 
                    else:
                        element["Multiple values"] = "True"
            else:
                for element in data:
                    element["Multiple values"] = "s"

        return json.dumps(data)

    def count_characters(self, elements):
        return [len(element) for element in elements]

    def is_characters_alright(self):
        json_data = self.is_multiple()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Number of characters"] = self.count_characters(data["Text"])
            return json.dumps(data)
        elif isinstance(data, list):
            for entry in data:
                entry["Number of characters"] = len(entry["Text"])
            return json.dumps(data)
        return json.dumps([])

    
    def is_duplicate(self):
       
       pass

   
class Title(AnalyseData):

    def analyse_missing(self):
        data = self.is_characters_alright()
        result_from_missing = 0
        if all(data.loc['Missing value'] == 'False'):
            result_from_missing = 5
        else:
            result_from_missing = 0
        return result_from_missing

    def analyse_length(self):
        data = self.is_characters_alright()
        result_from_title = 0
        for num_chars_list in data.loc['Number of characters']:
            for num_chars in num_chars_list:
                if num_chars <= 30:
                    result_from_title += 0
                elif num_chars >= 70:
                    result_from_title += 0
                else:
                    result_from_title += 5
        return result_from_title

    def analyse_multiple(self):
        data = self.is_characters_alright()
        result_from_multiple = 0

        if all(data.loc['Multiple values'] == 'False'):
            result_from_multiple = 5
        else:
            result_from_multiple = 0
        return result_from_multiple

    def is_title_thesame_as_h1():
        
        pass
    def title_result(self):
        result_from_missing = self.analyse_missing()
        result_from_title = self.analyse_length()
        result_from_multiple = self.analyse_multiple()
        
        result = result_from_missing + result_from_title + result_from_multiple
        return result
class Headings(AnalyseData):

    def analyse_missing(self):
        data = self.is_characters_alright()
        result_from_missing = 0
        if all(data.loc['Missing value'] == 'False'):
            result_from_missing = 3
        else:
            result_from_missing = 0
        return result_from_missing

    def analyse_length(self):
        data = self.is_characters_alright()
        print(data)
        result_from_title = 0
        for num_chars_list in data.loc['Number of characters']:
            for num_chars in num_chars_list:
                if num_chars <= 30:
                    result_from_title += 0
                elif num_chars >= 70:
                    result_from_title += 0
                else:
                    result_from_title += 5
        return result_from_title

    def analyse_multiple(self):
        data = self.is_characters_alright()
        result_from_multiple = 0

        if all(data.loc['Multiple values'] == 'False'):
            result_from_multiple = 2
        else:
            result_from_multiple = 0
        return result_from_multiple

    #work in progress
    def is_h1_thefirst_heading(self):
        
        data = AnalyseData.is_right_file(DataFromHtmlStructure.get_headings(self))
        result_from_firstheading = 0

        if data.loc['0','Headings'] == 'h1':
            result_from_firstheading == 2
        else:
            result_from_firstheading = 0
        return result_from_firstheading

    def title_result(self):
        result_from_missing = self.analyse_missing()
        result_from_title = self.analyse_length()
        result_from_multiple = self.analyse_multiple()
        #result_from_firstheading = self.is_h1_thefirst_heading()
        
        result = result_from_missing + result_from_title + result_from_multiple #+ result_from_firstheading
        return result


class MetaDescription(AnalyseData):


    pass


        
    
        
