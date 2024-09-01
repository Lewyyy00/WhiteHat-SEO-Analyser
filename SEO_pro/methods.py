from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *

def stopwordsss(url):
    data = DataFromUrl(url)
    return data.get_website_language()

def choicer(data, keywords, website_language):    
    if keywords is None:
        evaluator = Results(data)
        return evaluator.title_result()
    else:
        if isinstance(data, dict):
            headings_list = []
            print('j')
            for j in data.values(): #path for headings 
                for data in j:
                    text_analyser = TextAnalyzer(data, website_language)
                    ta = text_analyser.sentence_tokenize()
                    headings_list.append(ta)
            return headings_list
        
        elif len(data) > 3: #path for content and alt_content if keywords are not none (content and alt_content go always with keywords)
            print('i')
            text_analyser = TextAnalyzer(data, website_language)
            return text_analyser.keyword_density(keywords, data, website_language)
                
        else: #path for title, meta description 
            print('c')
            text_analyser = TextAnalyzer(data, website_language)
            return text_analyser.is_keyword_in_element(keywords, data, website_language)
                
@handle_request_errors
def make_right_choice(url, option, keywords = None):

    data_from_html = None
    data = None
    
    if option in ['title', 'meta_description', 'headings']:
        data_from_html = DataFromHtmlStructure(url)
    elif option in ['content', 'alt_content']:
        data_from_html = DataFromTextStructures(url)
    elif option == 'url_content':
        data_from_html = DataFromUrl(url)

    website_language = stopwordsss(url)

    if option == 'title':
        data = data_from_html.get_title()
    elif option == 'meta_description':
        data = data_from_html.get_meta_description()
    elif option == 'headings':
        data = data_from_html.get_headings()
    elif option == 'content':
        data = data_from_html.get_content()
    elif option == 'alt_content':
        data = data_from_html.get_all_alt_texts()
    elif option == 'url_content':
        if keywords is None:
            return data_from_html.find_any_not_ascii_letters() #url goes without choicer if we check keywords
        else:
            split_url = data_from_html.split_url() 
            return TextAnalyzer(split_url).is_keyword_in_element(keywords, split_url, website_language) 

    return choicer(data, keywords, website_language)


def links_choice(url, option):
    all_links = UrlStructure(url)

    if option == 'All valid links':
        data = all_links.get_all_200_links()
    elif option == 'All not valid links':
        data = all_links.get_all_not_valid_links()
    elif option == 'All domain links':
        data = all_links.method_choicer()
    elif option == 'All canonical links':
        data = all_links.get_all_canonical_links()
    elif option == 'All external links':
        data = all_links.get_all_external_links()

    return data



#z = make_right_choice('https://wazdan.com', 'title')
#z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'content','load balancer')
#z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'alt_content', 'load')
#z = make_right_choice('https://la-finestra.pl/', 'headings','menu')
#z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'meta_description', 'load')
z = make_right_choice('https://www.ovhcloud.com/pl/public-cloud/what-load-balancing/', 'url_content')

print(z)

