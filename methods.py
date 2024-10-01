from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from WebsiteTimeAndSecurity import *

def stopwordsss(url):
    data = DataFromUrl(url)
    return data.get_website_language()

def choicer(data, keywords, website_language):    

    """The function that pilots the API request depends on the needs. Basically there is a choice 
    where you just want An analyse for yor data (title, headings etc.) and a path for analysing keywords 
    in the choosen data"""

    if keywords is None:
        evaluator = AnalyseData(data)
        return evaluator.is_characters_alright()
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
            'metadescription': data_from_html.get_meta_description(),
            'headings': data_from_html.get_headings(), 
        }
    else:
         data = {
            'title': data_from_html.get_title(),
            'metadescription': data_from_html.get_meta_description(),
            'headings': data_from_html.get_headings(),
            'content': data_from_text.get_content(),
            'altcontent': data_from_text.get_all_alt_texts(), 
            'urlcontent': data_from_url.find_any_not_ascii_letters() 
        } 
    return data

# a lot of unneccesey code, somehow this function could be joined with make_right_choice
@handle_request_errors
def object_choicer(url, option):

    data_from_html = None
    data = None
    
    if option in ['title', 'metadescription', 'headings']:
        data_from_html = DataFromHtmlStructure(url)
    elif option in ['content', 'altcontent']:
        data_from_html = DataFromTextStructures(url)
    elif option == 'urlcontent':
        data_from_html = DataFromUrl(url)

    if option == 'title':
        data = data_from_html.get_title()
    elif option == 'metadescription':
        data = data_from_html.get_meta_description()
    elif option == 'headings':
        data = data_from_html.get_headings()
    elif option == 'content':
        data = data_from_html.get_content()
    elif option == 'altcontent':
        data = data_from_html.get_all_alt_texts()
    elif option == 'urlcontent':
        data = data_from_html.split_url() 

    return data
    
@handle_request_errors
def make_right_choice(url, option, keywords = None):

    data_from_html = None
    data = None
    
    if option in ['title', 'metadescription', 'headings']:
        data_from_html = DataFromHtmlStructure(url)
    elif option in ['content', 'altcontent']:
        data_from_html = DataFromTextStructures(url)
    elif option == 'urlcontent':
        data_from_html = DataFromUrl(url)

    website_language = stopwordsss(url)

    if option == 'title':
        data = data_from_html.get_title()
    elif option == 'metadescription':
        data = data_from_html.get_meta_description()
    elif option == 'headings':
        data = data_from_html.get_headings()
    elif option == 'content':
        data = data_from_html.get_content()
    elif option == 'altcontent':
        data = data_from_html.get_all_alt_texts()
    elif option == 'urlcontent':
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

    if option == 'valid':
        data = all_links.get_all_200_links()
    elif option == 'notvalid':
        data = all_links.get_all_not_valid_links()
    elif option == 'domain':
        data = all_links.method_choicer()
    elif option == 'canonical':
        data = all_links.get_all_canonical_links()
    elif option == 'external':
        data = all_links.get_all_external_links()
    elif option == 'status':
        data = all_links.evaluate_all_links()
    """elif option == 'all':
        data = {
            #'All valid links': all_links.get_all_200_links(),
            #'All not valid links': all_links.get_all_not_valid_links(),
            'All domain links': all_links.method_choicer(),
            'All canonical links': all_links.get_all_canonical_links(),
            'All external links': all_links.get_all_external_links()
        }"""

    return data

def keyword_options(url, option, analysingobject, querytext = None, n=None):

    """Some of these methods are unnecessary, becasue in choicer() we got a path for analysing 
    keywords in the text. Anyway, I put it here to bring some order"""

    laguange = stopwordsss(url)
    print(analysingobject)
    text = object_choicer(url,analysingobject) 
    text_analyser = TextAnalyzer(text, laguange)
    

    if option == 'mostpopularngrams':
        data = text_analyser.find_most_common_ngrams(n)
    elif option == 'ngramsinquery':
        data = text_analyser.is_ngrams_in_query(querytext, text, n)
    elif option == 'contentwithkeywords':
        data = text_analyser.is_keyword_in_element(querytext, text, laguange)
    elif option == 'keywordsdensity':
        data = text_analyser.keyword_density(querytext, text, laguange)
    elif option == 'all':
        data = {
            'Most popular Ngrams': text_analyser.find_most_common_ngrams(n), #does not work properly 
            'Ngrams in query': text_analyser.is_ngrams_in_query(querytext, text, n), #does not work properly
            'Keywords in paragraphs': text_analyser.is_keyword_in_element(querytext, text, laguange),
            'Keyword_density': text_analyser.keyword_density(querytext, text, laguange), 
            'Elements': text,
            'Analysing object': analysingobject
        }
    
    return data

def time_options(url, option):    
    timer = PageLoadTimerAnaylyser()
    if option == 'websitetimeload':
        load_time = timer.measure_webiste_load_time(url)
        
        timer.close_browser()
        return load_time  

    #does not work
    elif option == 'filecorrectness':
        load_time = timer.is_each_file_loaded(url)
        
        timer.close_browser()
        return load_time  

    else: #add all 
        pass    

def check_duplicates(url, method, links=None, threshold=None):
    #add more options 
    if method == 'title':
        data = str('get_title')
    elif method == 'meta':
        data = str('get_meta_description')
    elif method == 'content':
        data = str('content')
        

    else:
        raise ValueError("Invalid method. Choose either 'title' or 'meta'.")

    if links is None:
        links = UrlStructure(url).get_all_canonical_links()

    if threshold is None:
        threshold = 0.1

    return SearchDuplicates(data).is_duplicate(links, data, threshold=threshold)



    
  