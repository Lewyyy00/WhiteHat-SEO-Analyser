import requests 

from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')

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






