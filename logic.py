import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')

class WebsiteData:
    def __init__(self, website):
        self.website = website

    def get_soup(self):
        response = requests.get(self.website)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    """def get_all_links(self):
        soup = self.get_soup()
        
        links = [a.get('href') for a in soup.find_all('a', href = True)]
        full_url = [urljoin(self.website, link) for link in links]

        return full_url"""
    
    def get_all_links(self):
        soup = self.get_soup()
        links = soup.find_all('a', href = True) #szuka wszytskich linków, gdzie jest spełniony warunek href = true

        LinksGroup = set()
        for link in links:
            full_url = urljoin(self.website, link['href'])
            LinksGroup.add(full_url)
        return LinksGroup


    def get_all_404_links(self):
        links = self.get_all_links()
        links_404 = []
        try:    #konieczne inaczej mieli mega dług
            for link in links:
                link_response = requests.get(link, timeout=1)
                if link_response.status_code == 404:
                    links_404.append(link)
        except requests.exceptions.Timeout:
            print(f"Timeout checking {link}")

        print(links_404)
        return links_404

    
    def get_title(self):
        try:
            soup = self.get_soup()
            title_tag = soup.title
            title = title_tag.string
            print(title)
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
    

class TextAnalyzer:
    def __init__(self, text):
        self.text = text

    def preprocess_text(self):
        if isinstance(self.text, list):
            processed_texts = [self._preprocess_single_text(t) for t in self.text]
            return processed_texts
        elif isinstance(self.text, str):  
            text = self.text.split()
            processed_texts = [self._preprocess_single_text(word) for word in text]
            return processed_texts
        else:
            return self._preprocess_single_text(self.text)

    def _preprocess_single_text(self, text):
        preprocesed_text = text.lower()  
        preprocesed_text = re.sub(r'\b\w{1}\b', '', preprocesed_text)  
        preprocesed_text = re.sub(r'\s+', ' ', preprocesed_text)  
        preprocesed_text = re.sub(r'[^\w\s]', '', preprocesed_text)  
        return preprocesed_text
    
    def sentance_tokenize(self):
        preprocessed_texts = self.preprocess_text()
        stop_words = set(stopwords.words("english"))
        
        filtered_sentences = []

        for sentence in preprocessed_texts:
            words = word_tokenize(sentence)
            filtered_sentence = ' '.join([word for word in words if word not in stop_words]) #there is a list of lists with each word without ' '.join()
            filtered_sentences.append(filtered_sentence)

        for i in filtered_sentences:
            if len(i) == 0:
                filtered_sentences.remove(i)
        return filtered_sentences


class KeyWordFinder:
    def __init__(self, query):
        self.query = query
    
    def get_key_words(self, query):
        key_words = [word.lower() for word in query.split()]
        return key_words
    
    
    def find_key_words_in_title(self, title):
        title_keywords = self.get_key_words(title)
        query_keywords = self.get_key_words(self.query)

        title_keywords = [keyword for keyword in title_keywords if keyword in query_keywords]
        return title_keywords
       

    def find_key_words_in_url(self, url):
        key_words = self.get_key_words(self.query) 
        parsed_url = urlparse(url)
        url_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
        found_keywords =[]

        for part in url_parts:
            for keyword in key_words:
                if keyword in part:
                    found_keywords.append(keyword)
        return list(set(found_keywords))
    
    def find_key_words_in_all_urls(self, urls):
        key_words = self.get_key_words(self.query) 
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


"""
website_data = WebsiteData('https://www.szymonslowik.pl/seo-co-to-jest/')
paragraphs = website_data.get_paragraphs()
headings = website_data.get_headings()
kf = KeyWordFinder('Is a wazdan realiable company?')
ta = TextAnalyzer('https://www.szymonslowik.pl/seo-co-to-jest/')
i = ta.preprocess_text()
y = ta.sentance_tokenize()

print(y)
#title = website_data.get_title()

#all_links = website_data.get_all_links()
#all_404 = website_data.get_all_404_links()

#kf_in_title = kf.find_key_words_in_title('reliable company webiste, wazdan, is,')
#kf_in_url = kf.find_key_words_in_all_urls(all_links)
#kf_in_all_urls = kf.find_key_words_in_all_urls('https://wazdan.com/')"""



#1 URL Structure

def split_url(url):
    url = re.sub(r'^https?:\/\/', '', url)
    url = re.sub(r'[\/\-_?&=]', ' ', url)
    potential_keywords = url.split()
    
    return potential_keywords

#czy są słowa kluczowe 
# to samo jest w metodzie find_key_words_in_title
def find_keywords_url(url, keywords):
    keywords_url = split_url(url)
    analyzer = TextAnalyzer(keywords)
    key_words = analyzer.sentance_tokenize()

    url_keywords = [keyword for keyword in keywords_url if any(key in keyword for key in key_words)]
    return url_keywords


x = split_url('https://www.szymonslowik.pl/seo-co-to-jest/')
print(x)
print('---')
#brak dynamicznych URL

#im krótsze URL tym lepiej 

#użycie - zamiast _
def analyze_url_hyphens(url):
    results = {}
    
    for url in urls:
        results[url] = '_' in url
    return results
    

y = analyze_url_hyphens('https://www.szymonslowik.pl/seo-co-to-jest/')
print(y)
#unikanie stopwords

#brak dużych liter