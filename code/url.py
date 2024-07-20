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
                return print(f'{url} has emphasis')
            else:
                return print(f'{url} does not have emphasis')

    def find_capital_letters(self):
        for i in self.url:
            if i.isupper():
                return f'{self.url} has capital letters'
        f'{self.url} does not have capital letters'

    def find_parameters(self):
        non_ascii_chars = [char for char in url if ord(char) > 127]
        return non_ascii_chars

    def get_all_links(self):
        soup = self.get_soup()
        links = soup.find_all('a', href=True)  # szuka wszystkich linków, gdzie jest spełniony warunek href=True
        links_200 = []
        error_links = {}  # Słownik do przechowywania błędnych linków i ich statusów
        
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
                else:
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
                
        return links_200, error_links
    
    def asses_results():
        


        pass




url = 'https://www.szymonslowik.pl/seo_co-to-jest/'
text = 'Jak wyszukac co to jest SEO?'

ta = TextAnalyzer(text)
keywords = ta.sentance_tokenize()
us = UrlStructure(url, keywords)

x = us.find_capital_letters()
print(x)

"""x = us.split_url()
print(x)
y = us.find_keywords_url()
print(y)
z = us.get_all_links()
print(z)"""
"""l = us.get_lenght_url()
print(l)
"""


