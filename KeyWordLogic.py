import requests 
from collections import Counter
from urllib.parse import urljoin, urlparse
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from values import polish_stopwords
nltk.download('stopwords')
nltk.download('punkt')
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TextAnalyzer:

    """This class is designed to preprocess and tokenize text data, 
    supporting multiple input types including strings, lists, and dictionaries"""

    def __init__(self, text, language = None):
        self.text = text
        self.language = language

    def preprocess_text(self):

        """The preprocess_text() method handles different text formats, performing cleaning 
        tasks such as lowercasing, removing punctuation, and filtering out short words"""

        if isinstance(self.text, list):
            processed_texts = [self._preprocess_single_text(t) for t in self.text]
            return processed_texts
        elif isinstance(self.text, str):  
            text = self.text.split()
            processed_texts = [self._preprocess_single_text(word) for word in text]
            return processed_texts
        elif isinstance(self.text, dict):  
            all_processed_texts = []
            for key, texts in self.text.items():
                print(texts)
                
                processed_texts = [self._preprocess_single_text(t) for t in texts]
                all_processed_texts.extend(processed_texts)
            return all_processed_texts
                
        else:
            return self._preprocess_single_text(self.text)

    def _preprocess_single_text(self, text):
        if text is None:
            return ''
        else:
            preprocesed_text = text.lower()  
            preprocesed_text = re.sub(r'\b\w{1}\b', '', preprocesed_text)  
            preprocesed_text = re.sub(r'\s+', ' ', preprocesed_text)  
            preprocesed_text = re.sub(r'[^\w\s]', '', preprocesed_text)  
            return preprocesed_text

    def sentence_tokenize(self):

        """The sentence_tokenize() method tokenizes the text into individual words while removing stopwords 
        based on the specified language (Only english and polish are available at this moment). This class is used for preparing 
        text for natural language processing tasks like is_keyword_in_element() and keyword_density()"""

        preprocessed_texts = self.preprocess_text()

        logging.debug(f"sentence_tokenize - preprocessed_texts:{preprocessed_texts}")

        if self.language is None:
            pass
        else:
            if 'en' in self.language or 'GB' in self.language:
                stop_words = set(stopwords.words("english"))
            else:
                stop_words = polish_stopwords
        
        filtered_sentences = []

        for sentence in preprocessed_texts:
            words = word_tokenize(sentence)
            
            logging.debug(f"sentence_tokenize - words:{words}")

            if self.language is None:
                filtered_sentence = ' '.join([word for word in words]) #there is a list of lists with each word without ' '.join()
                filtered_sentences.append(filtered_sentence)
            else:
                filtered_sentence = ' '.join([word for word in words if word not in stop_words]) #there is a list of lists with each word without ' '.join()
                filtered_sentences.append(filtered_sentence)

        for i in filtered_sentences:
            if len(i) == 0:
                filtered_sentences.remove(i)

        logging.debug(f"sentence_tokenize - filtered_sentences:{filtered_sentences}")

        return filtered_sentences
    
    def sentence_chunking(self):
        pass

    def is_single_word_list(self, list):
        return all(len(word_tokenize(item)) == 1 for item in list)

    def generate_ngrams(self, n):
        sentences = self.sentence_tokenize()

        logging.debug(f"generate_ngrams - sentences:{sentences}")

        ngram_list = []
        n = int(n)
        
        if self.is_single_word_list(sentences) == True:
            ngram_list = list(ngrams(sentences, n))
            return ngram_list
        else:
            for sentence in sentences:
                words = word_tokenize(sentence)
                ngrams_generated = list(ngrams(words, n))
                ngram_list.extend(ngrams_generated)
            return ngram_list
    
    def find_most_common_ngrams(self, n):
        data = self.generate_ngrams(n)

        logging.debug(f"find_most_common_ngrams - data:{data}")

        ngram_counts = Counter(data)
        most_common_ngrams = ngram_counts.most_common(10)
        return most_common_ngrams
    
    @staticmethod
    def is_ngrams_in_query(querytext, text, n):

        logging.debug(f"is_ngrams_in_query - querytext:{querytext}")
        logging.debug(f"is_ngrams_in_query - text:{text}")

        analyzer_query = TextAnalyzer(querytext)
        analyzer_text = TextAnalyzer(text)
        text_from_query = analyzer_query.generate_ngrams(n)
        text_from_page = analyzer_text.generate_ngrams(n)
        
        logging.debug(f"is_ngrams_in_query - text from query:{text_from_query}")
        logging.debug(f"is_ngrams_in_query - text from page:{text_from_query}")

        common_elements = []

        for element in text_from_query:
            if element in text_from_page:
                common_elements.append(element)
        return common_elements
    
    @staticmethod
    def is_keyword_in_element(querytext, text, website_language):

        logging.debug(f"is_keyword_in_element - querytext:{querytext}")
        logging.debug(f"is_keyword_in_element - text:{text}")

        analyzer_query = TextAnalyzer(querytext, website_language)
        analyzer_text = TextAnalyzer(text, website_language)
        text_from_query = analyzer_query.sentence_tokenize()
        text_from_page = analyzer_text.sentence_tokenize()

        logging.debug(f"is_keyword_in_element - text from query:{text_from_query}")
        logging.debug(f"is_keyword_in_element - text from page:{text_from_query}")

        text_from_query = [x for x in text_from_query if x]
        text_from_page = [x for x in text_from_page if x]

        if len(text_from_page) == 1: 
            words_from_page = text_from_page[0].split()
        else: 
            words_from_page = text_from_page

        common_elements = [element for element in words_from_page if any(x in element for x in text_from_query)]
        return common_elements
    
    @staticmethod
    def keyword_density(querytext, text, website_language):

        logging.debug(f"keyword_density - querytext: {querytext}")
        logging.debug(f"keyword_density - text: {text}")

        analyzer_query = TextAnalyzer(querytext, website_language)
        analyzer_text = TextAnalyzer(text, website_language)
        text_from_query = analyzer_query.sentence_tokenize()
        text_from_page = analyzer_text.sentence_tokenize()

        logging.debug(f"keyword_density - text from query: {text_from_query}")
        logging.debug(f"keyword_density - text from page: {text_from_page}")

        ta = ' '.join(text_from_page)
        x = len(ta.split())
        counter = 0
    
        for element in text_from_query:
            count = ta.count(element)
            counter += count
        
        density = round((counter/x) * 100, 2) 
        return f'{density}%'
     





