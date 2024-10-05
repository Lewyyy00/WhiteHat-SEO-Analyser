from data_evaluator import *

"""
Each SEO element such as (title, headings etc.) in addition to the general methods presented 
in data_evaluator.py should also be checked for specific ones that will be written underneath
in the nearest future. 

Right now there are only leftovers from the first idea.

"""

#In progress
class Results(AnalyseData):

    def path_selector(self):
        data = self.is_characters_alright()
        if isinstance(self.data, dict):
            pass


        pass

    def analyse_missing(self):
        data = self.is_characters_alright()
        result_from_missing = 0

        if isinstance(data, dict):
            if data['Missing value'] == ["False"]:
                result_from_missing = 5
                data['Points from missing'] = result_from_missing
                return data
            else:
                result_from_missing = 0
                data['Points from missing'] = result_from_missing
                return data
        else:
            for element in data:
                if element['Missing value'] == 'False':
                    result_from_missing = 5
                    element['Points from missing'] = result_from_missing
                else:
                    result_from_missing = 0
                    element['Points from missing'] = result_from_missing
                return data

    def analyse_length(self):
        data = self.analyse_missing()
        result_from_title = 0
        
        if isinstance(data, dict):
            num_chars = data['Number of characters']
            for num_chars in num_chars:
                if 30 < num_chars < 70:
                    result_from_title = 5
            data['Points from length'] = result_from_title
            return data
        else:
            for element in data:
                num_chars = element['Number of characters']
                if 30 < num_chars < 70:
                    result_from_title = 5
                element['Points from length'] = result_from_title
                return data

    def analyse_multiple(self):
        data = self.analyse_length()
        result_from_multiple = 0
        
        if isinstance(data, dict):
            if data['Multiple values'] == ["False"]:
                result_from_multiple = 5
                data['Points from multiple'] = result_from_multiple
                return data
            else:
                result_from_multiple = 0
                data['Points from multiple'] = result_from_multiple
                return data
        else:
            for element in data:
                if element['Multiple values'] == 'False':
                    result_from_multiple = 5
                    element['Points from multiple'] = result_from_multiple
                else:
                    result_from_multiple = 0
                    element['Points from multiple'] = result_from_multiple
            return data

    def title_result(self):
        data = self.analyse_multiple()

        if isinstance(data, dict):
            data['Overall points'] = data['Points from missing'] + data['Points from length'] + data['Points from multiple']  
            return data
        else:
            for element in data:
                element['Overall points'] = element['Points from missing'] + element['Points from length'] + element['Points from multiple']  
        return data

#In Progress
class Headings(AnalyseData):

    def analyse_missing(self):
        data = self.is_characters_alright()
        result_from_missing = 0

        if isinstance(data, list):
            if data['Missing value'] == ["False"]:
                result_from_missing = 3
                data['Points from missing'] = result_from_missing
                return data
            else:
                result_from_missing = 0
                data['Points from missing'] = result_from_missing
                return data
        else:
            for element in data:
                if element['Missing value'] == 'False':
                    result_from_missing = 3
                    element['Points from missing'] = result_from_missing
                else:
                    result_from_missing = 0
                    element['Points from missing'] = result_from_missing
            return data

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




