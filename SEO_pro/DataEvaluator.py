from DataCrawler import *
import language_tool_python

class AnalyseData:
    def __init__(self, data):
        self.data = data

    def is_right_file(self):
        if isinstance(self.data, list) or isinstance(self.data, str):
            newdata = {
                "Text": self.data 
            }
            json_data = json.dumps(newdata)
            return json_data
        
        elif isinstance(self.data, dict):  
            rows = []
            for heading, texts in self.data.items():
                for text in texts:
                    rows.append({"Headings": heading, "Text": text})

            json_data = json.dumps(rows)
            return json_data
        else:
            return json.dumps([])
            
    def count_words(self, text):
        words = text.split()
        return len(words)

    def count_words_in_list(self, elements):
        numer_of_words = [self.count_words(element) for element in elements]
        return numer_of_words

#needs to be fixed
    def is_length_alright(self):
        json_data = self.is_right_file()
        data = json.loads(json_data)
        if isinstance(data, dict) and "Text" in data:
            texts = data["Text"]
            lengths = [len(text) for text in texts]
            elements_in_list = [len(texts)]
            word_counts = [self.count_words(text) for text in texts]
            result = {
                "Text": texts,
                "length": lengths,
                "word_count": word_counts,
                "elements": elements_in_list
            }
            return json.dumps(result)
        elif isinstance(data, list):
            for element in data:
                element["length"] = len(element["Text"])
                element["word_count"] = self.count_words(element["Text"])
            return json.dumps(data)
        return json.dumps([])

    def is_missing(self):
        json_data = self.is_length_alright()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Missing value"] = [length == 0 for length in data["length"]]
            data["Missing value"] = ["True" if x else "False" for x in data["Missing value"]]
            return json.dumps(data)
        elif isinstance(data, list):
            for element in data:
                element["Missing value"] = "True" if element["length"] == 0 else "False"
            return json.dumps(data)
        return json.dumps([])

    def is_multiple(self):
        json_data = self.is_missing()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Multiple values"] = [length != 1 for length in data["elements"]]
            data["Multiple values"] = ["True" if x else "False" for x in data["Multiple values"]]
            return json.dumps(data)
        elif isinstance(data, list):
            headings = [d['Headings'] for d in data]
            amount_of_headings = Counter(headings)

            if amount_of_headings.get('h1', 0) == 1:
                for element in data:
                    if element.get('Headings') == 'h1':
                        element["Multiple values"] = "False"
                    elif element.get('Headings') != 'h1':
                        element["Multiple values"] = "does not influance SEO" #change to sth else 
                    else:
                        element["Multiple values"] = "True"
            else:
                for element in data:
                    element["Multiple values"] = "s"

        return json.dumps(data)

    def count_characters(self, elements):
        return [len(element) for element in elements]

    def is_characters_alright(self):
        json_data = self.is_multiple()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data["Number of characters"] = self.count_characters(data["Text"])
            return json.dumps(data)
        elif isinstance(data, list):
            for entry in data:
                entry["Number of characters"] = len(entry["Text"])
            return json.dumps(data)
        return json.dumps([])

    
    def is_duplicate(self):
       
       pass

   
class Title(AnalyseData):

    def path_selector(self):
        data = self.is_characters_alright()
        if isinstance(self.data, dict):
            pass


        pass

    def analyse_missing(self):
        json_data = self.is_characters_alright()
        data = json.loads(json_data)
        result_from_missing = 0
        if isinstance(data, dict):
            if data['Missing value'] == ["False"]:
                result_from_missing = 5
                data['Points from missing'] = result_from_missing
                return json.dumps(data)
            else:
                result_from_missing = 0
                data['Points from missing'] = result_from_missing
                return json.dumps(data)
        else:
            for element in data:
                if element['Missing value'] == 'False':
                    result_from_missing = 5
                    element['Points from missing'] = result_from_missing
                else:
                    result_from_missing = 0
                    element['Points from missing'] = result_from_missing
            return json.dumps(data)

    def analyse_length(self):
        json_data = self.analyse_missing()
        data = json.loads(json_data)
        result_from_title = 0
        
        if isinstance(data, dict):
            num_chars = data['Number of characters']
            for num_chars in num_chars:
                if 30 < num_chars < 70:
                    result_from_title = 5
            data['Points from length'] = result_from_title
            return json.dumps(data)
        else:
            for element in data:
                num_chars = element['Number of characters']
                if 30 < num_chars < 70:
                    result_from_title = 5
                element['Points from length'] = result_from_title
            return json.dumps(data)

    def analyse_multiple(self):
        json_data = self.analyse_length()
        data = json.loads(json_data)
        result_from_multiple = 0
        
        if isinstance(data, dict):
            if data['Multiple values'] == ["False"]:
                result_from_multiple = 5
                data['Points from multiple'] = result_from_multiple
                return json.dumps(data)
            else:
                result_from_multiple = 0
                data['Points from multiple'] = result_from_multiple
                return json.dumps(data)
        else:
            for element in data:
                if element['Multiple values'] == 'False':
                    result_from_multiple = 5
                    element['Points from multiple'] = result_from_multiple
                else:
                    result_from_multiple = 0
                    element['Points from multiple'] = result_from_multiple
            return json.dumps(data)

    def is_title_thesame_as_h1():
        
        pass
    def title_result(self):
        json_data = self.analyse_multiple()
        data = json.loads(json_data)

        if isinstance(data, dict):
            data['Overall points'] = data['Points from missing'] + data['Points from length'] + data['Points from multiple']  
            return json.dumps(data)
        else:
            for element in data:
                element['Overall points'] = element['Points from missing'] + element['Points from length'] + element['Points from multiple']  
            return json.dumps(data)

class Headings(AnalyseData):


    def analyse_missing(self):
        json_data = self.is_characters_alright()
        data = json.loads(json_data)
        result_from_missing = 0
        if isinstance(data, list):
            if data['Missing value'] == ["False"]:
                result_from_missing = 3
                data['Points from missing'] = result_from_missing
                return json.dumps(data)
            else:
                result_from_missing = 0
                data['Points from missing'] = result_from_missing
                return json.dumps(data)
        else:
            for element in data:
                if element['Missing value'] == 'False':
                    result_from_missing = 3
                    element['Points from missing'] = result_from_missing
                else:
                    result_from_missing = 0
                    element['Points from missing'] = result_from_missing
            return json.dumps(data)

    def analyse_missing(self):
        data = self.is_characters_alright()
        result_from_missing = 0
        if all(data.loc['Missing value'] == 'False'):
            result_from_missing = 3
        else:
            result_from_missing = 0
        return result_from_missing

    def analyse_length(self):
        data = self.is_characters_alright()
        result_from_title = 0
        for num_chars_list in data.loc['Number of characters']:
            for num_chars in num_chars_list:
                if num_chars <= 30:
                    result_from_title += 0
                elif num_chars >= 70:
                    result_from_title += 0
                else:
                    result_from_title += 5
        return result_from_title

    def analyse_multiple(self):
        data = self.is_characters_alright()
        result_from_multiple = 0

        if all(data.loc['Multiple values'] == 'False'):
            result_from_multiple = 2
        else:
            result_from_multiple = 0
        return result_from_multiple

    #work in progress
    def is_h1_thefirst_heading(self):
        
        data = AnalyseData.is_right_file(DataFromHtmlStructure.get_headings(self))
        result_from_firstheading = 0

        if data.loc['0','Headings'] == 'h1':
            result_from_firstheading == 2
        else:
            result_from_firstheading = 0
        return result_from_firstheading

    def title_result(self):
        result_from_missing = self.analyse_missing()
        result_from_title = self.analyse_length()
        result_from_multiple = self.analyse_multiple()
        #result_from_firstheading = self.is_h1_thefirst_heading()
        
        result = result_from_missing + result_from_title + result_from_multiple #+ result_from_firstheading
        return result


class MetaDescription(AnalyseData):


    pass

class Text():
    
    def __init__(self, data, language = 'en'):
        self.data = data
        self.language = language

    def check_language_correctness(self):
        tool = language_tool_python.LanguageTool(self.language)
        errors = []
        
        for paragraph in self.data:
            matches = tool.check(paragraph)
        if matches:
            errors.append((paragraph, matches))


