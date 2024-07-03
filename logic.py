import requests 
from bs4 import BeautifulSoup

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

#find_title('')

def find_headings(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    for i in headings:
        print(i.get_text())

def find_all_links(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href = True) #szuka wszytskich linków, gdzie jest spełniony warunek href = true
    for link in links:
        print(link['href'])

    LinksGroup = set()
    for link in links:
        LinksGroup.add(link)


#find_headings('https://wazdan.com/')
#find_headings('https://www.pragmaticplay.com/pl/')

find_all_links('https://wazdan.com/')