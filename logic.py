import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

'''
def analyse_site(site='https://miroslawmamczur.pl/beautifulsoup/'):
    try: 
        response = requests.get(site)
        response.raise_for_status() #raise for status pokazuje czy żdaniae się udało
        return(response.content)
    except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 


def find_key_words(promt = 'Najlepsze filmy w Polsce na wieczór - coś z BeautifulSoup'):
    key_words = promt.split()
    list_of_key_words = []
    for i in key_words:
        list_of_key_words.append(i)
    return list_of_key_words

#find_key_words()

def find_title(site):
    try:
        response = requests.get(site)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.title
        print(title_tag.string)
    except requests.exceptions.RequestException as error:
        print(f"błąd: {error}") 

    x = find_key_words(title_tag.string)
    y = find_key_words()
    for i in x:
        found_match = False #flaga pozwalająca śledzić czy dane słowo zostało już użyte
        for j in y:
            if i == j:
               print(f"Słowo kluczowe '{i}' występuje w tytule")
               found_match = True
               break
        if not found_match:
            print(f"Słowo kluczowe '{i}' nie występuje w tytule")
'''
'''
def find_headings(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    for i in headings:
        print(i.get_text())
'''

class WebCrawler:
    def __init__(self,site):
        self.site = site

    def find_all_links(self,site):
        response = requests.get(site)
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

    def find_key_words(self,promt = 'wazdan'):
        key_words = promt.split()
        list_of_key_words = []
        for i in key_words:
            list_of_key_words.append(i)
        print(list_of_key_words)
        return list_of_key_words
    
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

base_site = 'https://wazdan.com/' 
crawler = WebCrawler(base_site)
links = crawler.find_all_links(base_site)

def find_key_words_in_url(site):
    crawler = WebCrawler(site)
    key_words = crawler.find_key_words('wazdan news press losowe') 

    parsed_url = urlparse(site)
    url_parts = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment]
    found_keywords =[]

    for part in url_parts:
        for keyword in key_words:
            if keyword in part:
                found_keywords.append(keyword)
    return list(set(found_keywords))

x = find_key_words_in_url('https://wazdan.com/news/in-the-press/tragaperrasweb-interview-with-joanna-zdanowska-bieniek-the-secret-to-the-success-of-the-coins-series-and-expectations-for-score-the-jackpot')
print(x)
'''
if __name__ == '__main__':
    print(f'Znalezione linki:')
    for link in links:
        print(link)
    crawler.analyse_title_and_key_words()
'''

    