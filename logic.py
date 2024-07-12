import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from itertools import combinations


class WebsiteData:
    def __init__(self, website):
        self.website = website

    def get_soup(self):
        response = requests.get(self.website)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_all_links(self,website):
        soup = self.get_soup()

        links = soup.find_all('a', href = True) #szuka wszytskich linków, gdzie jest spełniony warunek href = true
       
        LinksGroup = set()
        for link in links:
            full_url = urljoin(website, link['href'])
            LinksGroup.add(full_url)
        return LinksGroup
    
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
        soup = self.get_soup()
        headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
        return [heading.text for heading in headings]
    
    def get_paragraphs(self):
        soup = self.get_soup()
        paragraphs = soup.find_all('p')
        return [paragraph.text for paragraph in paragraphs]
    
class KeyWordFinder:
    def __init__(self, query):
        self.query = query
    
    def get_key_words(self, query):
        key_words = query.split()
        #list_of_key_words = []
        #for i in key_words:
            #list_of_key_words.append(i)
        #return list_of_key_words
        return key_words
    
    
    def find_key_words_in_title(self, title):
        title_keywords = self.get_key_words(title)
        query_keywords = self.get_key_words()
        for keyword in title_keywords:
            found_match = False #flaga pozwalająca śledzić czy dane słowo zostało już użyte
            for keyword_2 in query_keywords:
                if keyword == keyword_2:
                    print(f"Słowo kluczowe '{keyword}' występuje w tytule")
                    found_match = True
                    break
                if not found_match:
                    print(f"Słowo kluczowe '{keyword_2}' nie występuje w tytule")

    def find_key_words_in_url(self, url):
        key_words = self.get_key_words() 
        parsed_url = urlparse(url)
        url_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
        found_keywords =[]

        for part in url_parts:
            for keyword in key_words:
                if keyword in part:
                    found_keywords.append(keyword)
        return list(set(found_keywords))
    
    def find_key_words_in_all_urls(self, urls):
        key_words = self.get_key_words() 
        #found_keywords = []
        for url in urls:
            keywords = self.find_key_words_in_url(url,keywords)
            print(f"URL: {url}")
            for keyword in key_words:
                if keyword in keywords:
                        print(f"Słowo kluczowe '{keyword}' jest w URL.")
                else:
                        print(f"Słowo kluczowe '{keyword}' NIE jest w URL.")
            print() 