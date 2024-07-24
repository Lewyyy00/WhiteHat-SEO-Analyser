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
nltk.download('stopwords')
nltk.download('punkt')


def handle_request_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.RequestException as error:
            print(error)
            return None
    return wrapper

#1 URL Structure
class UrlStructure:
    def __init__(self,url,keywords):
        self.url = url 
        self.keywords = keywords
        self.soup: Optional[BeautifulSoup] = None
        self._initialize_soup()

    def _initialize_soup(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status() 
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as error:
            print(error)
            self.soup = None

    def split_url(self):
        url = re.sub(r'^https?:\/\/', '', self.url)
        url = re.sub(r'[\/\-_?&=]', ' ', url)
        potential_keywords = url.split()
        return potential_keywords
     
    def find_keywords_url(self):
        keywords_url = self.split_url()
        url_keywords = [keyword for keyword in keywords_url if any(key in keyword for key in self.keywords)]
        return url_keywords
    
    def get_lenght_url(self):
        url_without_protocol  = re.sub(r'^https?:\/\/', '', self.url)
        lenght = len(url_without_protocol)
        return lenght
    
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

        for i in enumerate(self.url):
            if i == '_':
                return print(f'{self.url} has emphasis')
            else:
                return print(f'{self.url} does not have emphasis')

    def find_capital_letters(self):
        for i in self.url:
            if i.isupper():
                return f'{self.url} has capital letters'
        f'{self.url} does not have capital letters'

    def find_any_not_ascii_letters(self):
        non_ascii_chars = [char for char in self.url if ord(char) > 127]
        return non_ascii_chars
    
    @handle_request_errors
    def get_all_200_links(self):
        if self.soup:
            links = self.soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
            links_200 = []
            
            for link in links:
                href = link['href']
                full_url = urljoin(self.url, href)
                if not urlparse(full_url).scheme:
                    print(f"Invalid URL: {href}")
                    continue
                try:
                    link_response = requests.get(full_url, timeout=1)
                    if link_response.status_code == 200:
                        links_200.append(full_url)
                except requests.exceptions.Timeout:
                    print(f"Timeout checking {full_url}")
                except requests.exceptions.RequestException as e:
                    print(f"Error checking {full_url}: {e}")  
            return links_200
        return None
    
    @handle_request_errors
    def get_all_not_valid_links(self):
        if self.soup:
            links = self.soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
            error_links = {}  # Słownik do przechowywania błędnych linków i ich statusów
            
            for link in links:
                href = link['href']
                full_url = urljoin(self.url, href)
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
        parsed_url = urlparse(self.url)
        url_domain = parsed_url.netloc
        soup = self.get_soup()
        links = soup.find_all('a', href=True)
        internal_links = []

        for link in links:
            href = link['href']
            full_url = urljoin(self.url, href)
            potential_internal_link = urlparse(full_url)
            if url_domain == potential_internal_link.netloc:
                internal_links.append(full_url)
        return internal_links

    def get_all_external_links(self):
        parsed_url = urlparse(self.url)
        url_domain = parsed_url.netloc
        soup = self.get_soup()
        links = soup.find_all('a', href=True)
        external_links = []

        for link in links:
            href = link['href']
            full_url = urljoin(self.url, href)
            potential_internal_link = urlparse(full_url)
            if url_domain != potential_internal_link.netloc:
                external_links.append(link)
        return external_links

# HTML 
class DataFromHtmlStructure:
    def __init__(self, website):
        self.website = website
        self.soup: Optional[BeautifulSoup] = None
        self._initialize_soup()

    def _initialize_soup(self):
        try:
            response = requests.get(self.website)
            response.raise_for_status()  
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as error:
            print(error)
            self.soup = None
    
    @handle_request_errors
    def get_title(self):
        if self.soup:
            title_tag = self.soup.title
            title = title_tag.string
            return title
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
    def get_meta_description(self):
        if self.soup:
            meta_description = self.soup.find('meta', attrs={"name": "description"})

            if meta_description and 'content' in meta_description.attrs:
                return meta_description['content'] 
            else:
                return None
        return None
    
    @handle_request_errors
    def get_content(self):
        if self.soup:
            paragraphs = self.soup.find_all('p')
            return [paragraph.text for paragraph in paragraphs]
        return None
     
class AnalyseData():
    def __init__(self, data, website):
        self.data = data
        self.website = website

    def is_right_file(self):
        if isinstance(self.data, list):
            return self.data
        elif isinstance(self.data, dict):  
            rows = []
            for heading, texts in self.data.items():
                for text in texts:
                    rows.append((heading, text))

            df = pd.DataFrame(rows, columns=['Headings', 'Text'])
            return df['Text']
        else:
        
            pass
#in progress
    def is_missing(self):
        data = self.is_right_file()

        for i in data:
            if len(i) == 0:
                pass
            else:
                pass
            
#in progress
    def is_duplicate(self):
        urls = UrlStructure(self.website)
        

        internal_links = urls.get_all_internal_links()
        

        for i in internal_links:
            dfhs = DataFromHtmlStructure(i)
            title = dfhs.get_title()
            
            pass

    def lenght():

        pass

    def is_multiple():

        pass


    #Images 
class ImagesStructure:
    def __init__(self, website):
        self.website = website

    def get_all_images(self):
        images_list = []
        try:
            soup = self.get_soup()
            images = soup.find_all('img', attrs={"alt": ''})


        except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 
            return None
        
def make_df(url):
    keywords = 'cos'
    us = UrlStructure(url, keywords)
    linki = us.get_all_internal_links()
    data = []

    for link in linki:
        data_extractor = DataFromHtmlStructure(link)
        title = data_extractor.get_title()
        headings = data_extractor.get_headings()
        meta_description = data_extractor.get_meta_description()
        data.append({
            'URL': link,
            'Title': title,
            'Meta Description': meta_description,
            'Headings': headings,
            #'Content': content
        })

    df = pd.DataFrame(data)
    return df