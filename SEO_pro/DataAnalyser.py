from DataCrawler import *
from DataEvaluator import *

class TitleAnalyzer:
    def __init__(self):
        self.url = 'https://www.screamingfrog.co.uk/'
        self.url_structure = UrlStructure(self.url)
        

    def analyze_titles(self):
        links = self.url_structure.get_all_internal_links()
        print(links)
        for link in links:
            data_from_html = DataFromHtmlStructure(link)
            title = data_from_html.get_title()
            title_evaluator = Title(title)
            x= title_evaluator.title_result()
            print(x)


def main():
    analyzer = TitleAnalyzer()
    analyzer.analyze_titles()

if __name__ == "__main__":
    main()
