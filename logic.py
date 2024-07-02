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


find_title('https://miroslawmamczur.pl/beautifulsoup/')