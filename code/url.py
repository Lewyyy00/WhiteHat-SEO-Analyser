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
nltk.download('stopwords')
nltk.download('punkt')

#1 URL Structure
class UrlStructure:
    def __init__(self,url,keywords):
        self.url = url 
        self.keywords = keywords

    def split_url(self):
        url = re.sub(r'^https?:\/\/', '', self.url)
        url = re.sub(r'[\/\-_?&=]', ' ', url)
        potential_keywords = url.split()
        return potential_keywords
    
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def find_keywords_url(self):
        keywords_url = self.split_url()
        url_keywords = [keyword for keyword in keywords_url if any(key in keyword for key in self.keywords)]
        return url_keywords
    
    def get_lenght_url(self):
        url_without_protocol  = re.sub(r'^https?:\/\/', '', self.url)
        lenght = len(url_without_protocol)
        return lenght
    
    def get_website_language(self):
        soup = self.get_soup()
        html_tag = soup.find('html')

        if html_tag.has_attr("lang"):
            return html_tag['lang']
        
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

    def get_all_200_links(self):
        soup = self.get_soup()
        links = soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
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
    
    def get_all_not_valid_links(self):
        soup = self.get_soup()
        links = soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
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
                internal_links.append(link)
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

    def asses_results():
        
        pass

# HTML 
class DataFromHtmlStructure:
    def __init__(self, website):
        self.website = website

    def get_soup(self):
        response = requests.get(self.website)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_title(self):
        try:
            soup = self.get_soup()
            title_tag = soup.title
            title = title_tag.string
            return title
        except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 
            return None
        
    def get_headings(self):
        headings_dictionary = {}
        try:
            soup = self.get_soup()
            headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
            for heading in headings:
                if heading.name not in headings_dictionary:
                    headings_dictionary[heading.name] = []
                headings_dictionary[heading.name].append(heading.get_text())
            return headings_dictionary
        except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 
            return None
    
    def get_meta_description(self):
        try:
            soup = self.get_soup()
            meta_description = soup.find('meta', attrs={"name": "description"})

            if meta_description and 'content' in meta_description.attrs:
                return meta_description['content']
            else:
                return None
        except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 
            return None

    def get_content(self):
        soup = self.get_soup()
        paragraphs = soup.find_all('p')
        return [paragraph.text for paragraph in paragraphs]
     
class AnalyseData():
    def __init__(self, data):
        self.data = data

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

    def is_missing(self):
        data = self.is_right_file()

        for i in data:
            
            pass

    def is_duplicate():

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