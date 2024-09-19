from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from WebsiteTimeAndSecurity import *

def stopwordsss(url):
    data = DataFromUrl(url)
    return data.get_website_language()

def choicer(data, keywords, website_language):    
    if keywords is None:
        evaluator = Results(data)
        return evaluator.title_result()
    else:
        if isinstance(data, dict):
            headings_dict = {}
            print('j')
            for key, value in data.items(): #path for headings 
                headings_list = []
                for data in value:
                    text_analyser = TextAnalyzer(data, website_language)
                    ta = text_analyser.is_keyword_in_element(keywords, data, website_language)
                    headings_list.append(ta)

                headings_dict[key] = [x for x in headings_list if x] # removing empty List from List
            return headings_dict
        
        elif len(data) > 3: #path for content and alt_content if keywords are not none (content and alt_content go always with keywords)
            print('i')
            text_analyser = TextAnalyzer(data, website_language)
            data = {
                'kewords density': text_analyser.keyword_density(keywords, data, website_language)
            }
            return data
                
        else: #path for title, meta description 
            print('c')
            text_analyser = TextAnalyzer(data, website_language)
            data = {
                'keywords': text_analyser.is_keyword_in_element(keywords, data, website_language),
                'kewords density': text_analyser.keyword_density(keywords, data, website_language)
            }
            return data
        
def get_all_data(url, keywords = None):
    data_from_html = DataFromHtmlStructure(url)
    data_from_text = DataFromTextStructures(url)
    data_from_url = DataFromUrl(url)

    if keywords == None:
        data = {
            'title': data_from_html.get_title(),
            'meta_description': data_from_html.get_meta_description(),
            'headings': data_from_html.get_headings(), 
        }
    else:
         data = {
            'title': data_from_html.get_title(),
            'meta_description': data_from_html.get_meta_description(),
            'headings': data_from_html.get_headings(),
            'content': data_from_text.get_content(),
            'alt_content': data_from_text.get_all_alt_texts(), 
            'url_content': data_from_url.find_any_not_ascii_letters() 
        } 
    return data

# a lot of unneccesey code, somehow this function could be joined with make_right_choice
@handle_request_errors
def object_choicer(url, option):

    data_from_html = None
    data = None
    
    if option in ['title', 'meta_description', 'headings']:
        data_from_html = DataFromHtmlStructure(url)
    elif option in ['content', 'alt_content']:
        data_from_html = DataFromTextStructures(url)
    elif option == 'url_content':
        data_from_html = DataFromUrl(url)

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
        data = data_from_html.split_url() 

    return data
    
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
    elif option == 'all':
        data = get_all_data(url, keywords)
        all_results = {}
        for key, value in data.items():
            print(key)
            all_results[key] = choicer(value, keywords, website_language)

        if keywords == None:
            all_results['url'] = DataFromUrl(url).is_valid_protocol()
        
        return all_results
        
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
    elif option == 'All links statuses':
        data = all_links.evaluate_all_links()
    elif option == 'All':
        data = {
            #'All valid links': all_links.get_all_200_links(),
            #'All not valid links': all_links.get_all_not_valid_links(),
            'All domain links': all_links.method_choicer(),
            'All canonical links': all_links.get_all_canonical_links(),
            'All external links': all_links.get_all_external_links()
        }

    return data

def keyword_options(url, option, analysingobject, querytext = None, n=None):

    """Some of these methods are unnecessary, becasue in choicer() we got a path for analysing 
    keywords in the text. Anyway, I put it here to bring some order"""

    laguange = stopwordsss(url)
    print(analysingobject)
    text = object_choicer(url,analysingobject) #here must be an object which we want to analyse 
    print(text)
    text_analyser = TextAnalyzer(text)
    

    if option == 'Most popular Ngrams':
        data = text_analyser.find_most_common_ngrams(n)
    elif option == 'Ngrams in query':
        data = text_analyser.is_ngrams_in_query(querytext, text, n)
    elif option == 'Keywords in paragraphs':
        data = text_analyser.is_keyword_in_element(querytext, text, laguange)
        print(querytext)
        print(text)

    elif option == 'Keyword_density':
        data = text_analyser.keyword_density(querytext, text, laguange)
    elif option == 'All':
        data = {
            'Most popular Ngrams': text_analyser.find_most_common_ngrams(n),
            'Ngrams in query': text_analyser.is_ngrams_in_query(querytext, text, n),
            'Keywords in paragraphs': text_analyser.is_keyword_in_element(querytext, text, laguange),
            'Keyword_density': text_analyser.keyword_density(querytext, text, laguange),    
        }
    
    return data

def other_options(url, option):
    timer = PageLoadTimerAnaylyser(url)

    if option == 'website time load':
        load_time = timer.measure_webiste_load_time(url)
        timer.close_browser()    

    if option == 'language correctness':
        pass

    if option == 'find duplicates':
        pass

        return load_time
    else:
        pass    