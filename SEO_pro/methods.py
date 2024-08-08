from KeyWordLogic import *
from DataCrawler import *
from DataEvaluator import *
from DataAnalyser import *

@handle_request_errors
def make_right_choice(url, option):
    if option == 'title':
        data_from_html = DataFromHtmlStructure(url)
        title = data_from_html.get_title()
        
        text_analyser = TextAnalyzer(title)
        ta = text_analyser.sentence_tokenize()
        print(ta)

        title_evaluator = Title(title)
        x= title_evaluator.title_result()
        return x
    
    elif option == 'url_content':
        data_from_html = DataFromUrl(url)
        meta_description = data_from_html.find_any_not_ascii_letters()

    elif option == 'meta_description':
        data_from_html = DataFromHtmlStructure(url)
        meta_description = data_from_html.get_meta_description()

        text_analyser = TextAnalyzer(meta_description)
        ta = text_analyser.sentence_tokenize()
        print(ta)

        title_evaluator = Title(meta_description)
        x= title_evaluator.title_result()
        return x

    elif option == 'headings':
        data_from_html = DataFromHtmlStructure(url)
        headings = data_from_html.get_headings()

        for i, j in headings.items():
            for y in j:
                text_analyser = TextAnalyzer(y)
                ta = text_analyser.sentence_tokenize()
                print(ta)

        title_evaluator = Title(headings)
        x= title_evaluator.title_result()
        return x
    
    elif option == 'content':
        data_from_html = DataFromTextStructures(url)
        texts = data_from_html.get_content()

        text_analyser = TextAnalyzer(texts)
        x = text_analyser.sentence_tokenize()
        return x

    elif option == 'alt_content':
        data_from_html = DataFromTextStructures(url)
        alt_texts = data_from_html.get_all_alt_texts()

        text_analyser = TextAnalyzer(alt_texts)
        x = text_analyser.sentence_tokenize()
        return x

