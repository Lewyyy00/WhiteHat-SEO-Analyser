import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from KeyWordLogic import *
from values import polish_stopwords
import pandas as pd
from typing import Optional
import json
from collections import Counter
from functools import wraps
from sitemap import Sitemap
import concurrent.futures
nltk.download('stopwords')
nltk.download('punkt')

def handle_request_errors(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.exceptions.RequestException as error:
            print(error)
            return None
    return wrapper

def get_url_length(url):
    return len(url)

def sort_links(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        links = func(*args, **kwargs)

        if links is None:
            raise ValueError("NONE")

        sorted_links = sorted(links, key=get_url_length)
        return sorted_links
    return wrapper

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

#1 URL Structure
class UrlStructure(BaseStructure):
    #@sort_links
    @handle_request_errors
    def get_all_200_links(self):
        if self.soup:
            links = self.soup.find_all('a', href=True)
            links_200 = []
            
            for link in links:
                href = link['href']
                if href.startswith("https") or href.startswith("http"):
                    
                    full_url = urljoin(self.website, href)
                    print(full_url)
                    if not urlparse(full_url).scheme:
                        print(f"Invalid URL: {href}")
                        continue
            
                    link_response = requests.get(full_url, timeout=1)
                    if link_response.status_code == 200:
                        links_200.append(full_url)                 
            return links_200
        return []
    @handle_request_errors
    def get_sitemap_from_robots(self):
        if self.soup:
            if not self.website.endswith('/'):
                self.website += '/'
            
            robots_url = self.website + "robots.txt"
            response = requests.get(robots_url)
            
            if response.status_code == 200:
                content = response.text
                sitemap_links = []

                for line in content.splitlines():
                    if line.lower().startswith("sitemap:"):
                        sitemap_url = line.split(": ", 1)[1]
                        sitemap_links.append(sitemap_url)
                return sitemap_links
            else:
                print(f"Nie udało się pobrać {robots_url} (status code: {response.status_code})")
                return None
        return []
    
    def get_all_links_from_sitemap(self):
        data = ' '.join(self.get_sitemap_from_robots())
        response = requests.get(data)
        soup = BeautifulSoup(response.content, 'lxml-xml')  
        all_links = []
        sitemap_tags = soup.find_all('sitemap')

        for sitemap in sitemap_tags:
            sitemap_url = sitemap.find('loc').text
            sitemap_response = requests.get(sitemap_url)
            sitemap_soup = BeautifulSoup(sitemap_response.content, 'lxml-xml')
            
            url_tags = sitemap_soup.find_all('url')
            
            for url in url_tags:
                loc = url.find('loc').text
                all_links.append(loc)

        return all_links

    @sort_links
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
    @sort_links
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
            return set(internal_links)
        return None
    
    @sort_links
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
    
    def method_choicer(self):
        if len(self.get_all_links_from_sitemap()) == 0:
            return self.get_all_internal_links()
        else:
            return self.get_all_links_from_sitemap()

    def get_all_canonical_links(self):
        links = self.method_choicer()
        canonical_links = []

        for link in links:
            response = requests.get(link)
            response.raise_for_status()  # Raise an error for bad status codes
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in soup.find_all('link', rel='canonical'):
                if 'href' in tag.attrs:
                    canonical_links.append(tag['href'])
            
        return set(canonical_links)
    
    def link_status(self, link, max_retries = 3):
        
        """Sometimies when timeout is too low, the method returns too many timeouts, 
        that's why I use retries"""

        retries = 0
        while retries < max_retries:
            try:
                link_response = requests.get(link, timeout=2)
                return (link, link_response.status_code)
                
            except requests.exceptions.Timeout:
                retries += 1
                print(f"Timeout checking {link}")
                if retries == max_retries:
                    return (link, "Timeout")
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Error checking {link}: {e}")
                if retries == max_retries:
                    return (link, "Error")
        
    def evaluate_all_links(self):

        """Singlethreating takes a lot of time if there are a lot of links, 
        so multithreating is crucial. Thats why it is implemented """

        links = self.method_choicer()
        list_of_links_status = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.link_status, links)

        for link, status in results:
            list_of_links_status[link] = status

        return list_of_links_status
  
class DataFromUrl(BaseStructure):   

    def make_json(self):
        data = {'URL': [self.website]}
        return json.dumps(data)

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
        json_data = self.make_json()
        data = json.loads(json_data)
        url_without_protocol  = re.sub(r'^https?:\/\/', '', self.website)
        
        data['Url lenght'] = len(url_without_protocol)
        return json.dumps(data)

    def get_parsed_url(self):
        json_data = self.get_lenght_url()
        data = json.loads(json_data)
        parsed_url = urlparse(self.website)

        data['Url parts'] = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
        return json.dumps(data)
    
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
        json_data = self.get_parsed_url()
        data = json.loads(json_data)
        stop_words = self.get_stopwords_language()
        splited_url = self.split_url()

        data['List of stopwords in url'] = [element for element in splited_url if element in stop_words]
        return json.dumps(data)

    def analyze_url_hyphens(self):
        json_data = self.find_stopwords()
        data = json.loads(json_data)
        for i in self.website:
            if i == '_':
                data['Hyphens'] = 'True'
                return json.dumps(data)
        data['Hyphens'] = 'False'
        return json.dumps(data)

    def find_capital_letters(self):
        json_data = self.analyze_url_hyphens()
        data = json.loads(json_data)
        for i in self.website:
            if i.isupper():
                data['Capital letters'] = 'True'
                return json.dumps(data)
        data['Capital letters'] = 'False'
        return json.dumps(data)

    def find_any_not_ascii_letters(self):
        json_data = self.find_capital_letters()
        data = json.loads(json_data)
        non_ascii_chars = [char for char in self.website if ord(char) > 127]
        
        if len(non_ascii_chars) > 0:
            data['Not ASCII letters'] = 'True'
            return json.dumps(data)
        else:
            data['Not ASCII letters'] = 'False'
            return json.dumps(data)
        
    def is_valid_protocol(self):
        parsed_url = self.find_any_not_ascii_letters()
        data = json.loads(parsed_url)
        
        if data["Url parts"][0] == 'https':
            data["Https exist"] = 'True'
            return json.dumps(data)
        else:
            data["Https exist"] = 'False'
            return json.dumps(data)


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
    def get_all_h1(self, headingg = 'h1'):
        headings_dictionary = []
        if self.soup:
            headings = self.soup.find_all(headingg)
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
     
class DataFromTextStructures(BaseStructure):
    
    @handle_request_errors
    def get_content(self):
        if self.soup:
            paragraphs = self.soup.find_all('p')
            return [paragraph.text for paragraph in paragraphs]
        return None
    
    @handle_request_errors
    def get_page_content(self):
        if self.soup:
            paragraphs = self.soup.find_all('p')
            return ' '.join([paragraph.get_text() for paragraph in paragraphs])
        return None

    @staticmethod
    def get_content_from_urls(urls):
        contents = {}
        for url in urls:
            content_fetcher = DataFromTextStructures(url)
            content = content_fetcher.get_page_content()
            if content:
                contents[url] = content
        return contents

    @handle_request_errors
    def get_all_alt_texts(self):
        if self.soup:
            images = self.soup.find_all('img', src = True)
            return [alt_text.get('alt') for alt_text in images]
        return None

    

        
    
        
