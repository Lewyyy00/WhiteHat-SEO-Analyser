import requests 


def analyse_site(site='https://kodilla.com/pl'):
    try: 
        response = requests.get(site)
        response.raise_for_status() #raise for status pokazuje czy żdaniae się udało
        return(response.text)
    except requests.exceptions.RequestException as error:
            print(f"błąd: {error}") 

x = analyse_site()
print(x)