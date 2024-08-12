from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from DataAnalyser import *

def stopwordsss(url):
    data = DataFromUrl(url)
    lanuage = data.get_website_language()
    return lanuage

def choicer(data, keywords, website_language):
    print(data)
    print(type(data))
    if keywords is None:
        title_evaluator = Title(data)
        x= title_evaluator.title_result()
        return x
    else:
        if isinstance(data, dict):
            headings_list = []

            for j in data.values():
                for y in j:
                    text_analyser = TextAnalyzer(y, website_language)
                    ta = text_analyser.sentence_tokenize()
                    headings_list.append(ta)
            return headings_list
        else:
            text_analyser = TextAnalyzer(data, website_language)
            ta = text_analyser.sentence_tokenize()
            return ta
                
@handle_request_errors
def make_right_choice(url, option, keywords = None):
    if option == 'title':
        data_from_html = DataFromHtmlStructure(url)
        title = data_from_html.get_title()
        website_language = stopwordsss(url)
        
        x = choicer(title, keywords, website_language)
        return x

    elif option == 'meta_description':
        data_from_html = DataFromHtmlStructure(url)
        meta_description = data_from_html.get_meta_description()
        website_language = stopwordsss(url)
        
        x = choicer(meta_description, keywords, website_language)  
        return x
    
    elif option == 'headings':
        data_from_html = DataFromHtmlStructure(url)
        headings = data_from_html.get_headings()
        website_language = stopwordsss(url)
        
        x = choicer(headings, keywords, website_language)  
        return x
    
    elif option == 'content':
        data_from_html = DataFromTextStructures(url)
        texts = data_from_html.get_content()
        website_language = stopwordsss(url)
        
        x = choicer(texts, keywords, website_language)  
        return x

    elif option == 'alt_content':
        data_from_html = DataFromTextStructures(url)
        alt_texts = data_from_html.get_all_alt_texts()
        website_language = stopwordsss(url)
        
        x = choicer(alt_texts, keywords, website_language)  
        return x
     
    elif option == 'url_content':
        data_from_html = DataFromUrl(url)
        url_content = data_from_html.find_any_not_ascii_letters()
        website_language = stopwordsss(url)
        #fix
        url_json = data_from_html.make_json()
        url = url_json['URL'][0]

        if keywords is None:
            return url_content
        else:
            x = choicer(url, keywords, website_language) 
            return x


#x = make_right_choice('https://wazdan.com', 'title')
#f = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'content','witaj')
#c = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'alt_content')
#e = make_right_choice('https://la-finestra.pl/', 'headings')
#z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'meta_description')
z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'url_content', 'vcygfvug')

print(z)