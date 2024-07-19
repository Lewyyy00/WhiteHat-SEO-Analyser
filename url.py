import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from logic import *

#1 URL Structure

class UrlStructure:
    def __init__(self,url,keywords):
        self.url = url 
        self.keywords = keywords

    def split_url(self):
        url = re.sub(r'^https?:\/\/', '', self.url)
        url = re.sub(r'[\/\-_?&=]', ' ', self.url)
        potential_keywords = url.split()
        return potential_keywords
    
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    #czy są słowa kluczowe, to samo jest w metodzie find_key_words_in_title
    def find_keywords_url(self):
        
        keywords_url = self.split_url()
        
        url_keywords = [keyword for keyword in keywords_url if any(key in keyword for key in self.keywords)]
        return url_keywords
    
    def get_lenght_url(self):
        url_without_protocol  = re.sub(r'^https?:\/\/', '', self.url)
        lenght = len(url_without_protocol)
        return lenght
        
    def find_stopwords():
        

        pass

    def analyze_url_hyphens():


        pass

    def find_capital_letters():


        pass

    def find_parameters():


        pass

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

url = 'https://www.szymonslowik.pl/seo-co-to-jest/'
text = 'Jak wyszukac co to jest SEO?'

ta = TextAnalyzer(text)
keywords = ta.sentance_tokenize()
us = UrlStructure(url, keywords)

"""x = us.split_url()
print(x)
y = us.find_keywords_url()
print(y)
z = us.get_all_links()
print(z)"""
l = us.get_lenght_url()
print(l)



