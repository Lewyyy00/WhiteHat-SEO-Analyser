import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self,site):
        self.site = site

    def find_all_links(self,site):
        response = requests.get(self.site)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href = True) #szuka wszytskich linków, gdzie jest spełniony warunek href = true
       
        LinksGroup = set()
        for link in links:
            full_url = urljoin(site, link['href'])
            LinksGroup.add(full_url)
        return LinksGroup
    
    def find_title(self,site):
        try:
            response = requests.get(site)
            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.title
            title = title_tag.string
            return title
        except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 
            return None

    def find_key_words(self,prompt):
        key_words = prompt.split()
        #list_of_key_words = []
        #for i in key_words:
            #list_of_key_words.append(i)
        #return list_of_key_words
        return key_words
    
    def analyse_title_and_key_words(self):
        title = self.find_title(self.site)

        title_keywords = self.find_key_words(title)
        promt_keywords = self.find_key_words()
        for keyword in title_keywords:
            found_match = False #flaga pozwalająca śledzić czy dane słowo zostało już użyte
            for keyword_2 in promt_keywords:
                if keyword == keyword_2:
                    print(f"Słowo kluczowe '{keyword}' występuje w tytule")
                    found_match = True
                    break
                if not found_match:
                    print(f"Słowo kluczowe '{keyword_2}' nie występuje w tytule")

def find_key_words_in_url(site, keywords='wazdan news press losowe'):
    crawler = WebCrawler(site)
    key_words = crawler.find_key_words(keywords) 

    parsed_url = urlparse(site)
    url_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
    found_keywords =[]

    for part in url_parts:
        for keyword in key_words:
            if keyword in part:
                found_keywords.append(keyword)
    return list(set(found_keywords))

def find_key_words_in_all_urls(site, keywords='wazdan market games gaming'):
    crawler = WebCrawler(site)
    urls = crawler.find_all_links(site)
    key_words = crawler.find_key_words(keywords)
    
    #found_keywords = []
    for url in urls:
        keywords = find_key_words_in_url(url,keywords)
        print(f"URL: {url}")
        for keyword in key_words:
            if keyword in keywords:
                    print(f"Słowo kluczowe '{keyword}' jest w URL.")
            else:
                    print(f"Słowo kluczowe '{keyword}' NIE jest w URL.")
        print()  

def find_headings(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    return [heading.text for heading in headings]

def find_paragraphs(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return [paragraph.text for paragraph in paragraphs]



y = find_paragraphs('https://miroslawmamczur.pl/beautifulsoup/')    
print(y)
    
'''
if __name__ == '__main__':
    base_site = 'https://wazdan.com/' 
    crawler = WebCrawler(base_site)
    links = crawler.find_all_links(base_site)
    print(f'Znalezione linki:')
    for link in links:
        print(link)
    crawler.analyse_title_and_key_words()
'''

    