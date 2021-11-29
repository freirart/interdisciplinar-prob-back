import os
import pandas as pd
from unicodedata import normalize
from math import log

feminine_char = "F"
masculine_char = "M"

feminine_key = "Feminino"
masculine_key = "Masculino"

assumption_key = "Suposição"

name_key = "Nome"
gender_key = "Gênero"


class NaiveBayes(object):

    def __init__(self):
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'public'))
        self.set_initial_data()

    
    def set_initial_data(self):
        df = pd.read_csv(os.path.join(self.file_path, "nomes.csv"))

        names = df.to_dict("records")

        training_test_divisor = int(len(names)*0.64)
        test_validation_divisor = int(training_test_divisor + len(names)*0.18)

        self.names = names

        self.training_set = names[:training_test_divisor]
        self.training_set = names[:training_test_divisor]
        self.testing_set = names[training_test_divisor:test_validation_divisor]
        self.validation_set = names[test_validation_divisor:]


    def get_ending_char_probabilities_by_gender(self, my_set):
        char_set = ["a", "e", "o"]
        characteristics_dict = {}
        for char in char_set:
            characteristics_dict[char] = 0

        masculine_names_ending_in = characteristics_dict.copy()
        feminine_names_ending_in = characteristics_dict.copy()

        for item in my_set:
            item_name_ending_char = normalize("NFKD", item[name_key][-1:]).encode("ASCII","ignore").decode("ASCII")
            item_gender = item[gender_key]

            if item_name_ending_char in characteristics_dict:
                if item_gender == feminine_char:
                    feminine_names_ending_in[item_name_ending_char] += 1
                elif item_gender == masculine_char:
                    masculine_names_ending_in[item_name_ending_char] += 1

        num_of_feminine = len([item for item in my_set if item[gender_key] == feminine_char])
        num_of_masculine = len([item for item in my_set if item[gender_key] == masculine_char])

        ending_char_probabilities_by_gender = {}

        for char in char_set:
            curr_feminine_prob = (feminine_names_ending_in[char] / num_of_feminine) or 1
            curr_masculine_prob = (masculine_names_ending_in[char] / num_of_masculine) or 1
            
            ending_char_probabilities_by_gender[char] = {}

            ending_char_probabilities_by_gender[char][feminine_key] = curr_feminine_prob
            ending_char_probabilities_by_gender[char][masculine_key] = curr_masculine_prob


        return ending_char_probabilities_by_gender


    def get_model_info(self):
        analysis_table = self.get_ending_char_probabilities_by_gender(self.training_set)

        for item in self.training_set:
            item_name_ending_char = item[name_key][-1:]
            item[assumption_key] = self.get_assumption(item_name_ending_char, analysis_table)

        comparison = self.compare_assumption_with_reality(self.training_set)
        
        true_positive = comparison["true_positive"]
        true_negative = comparison["true_negative"]
        false_positive = comparison["false_positive"]
        false_negative = comparison["false_negative"]
        
        accuracy = {}
        precision = {}
        sensitivity = {}
        
        accuracy[feminine_key] = self.accuracy(true_positive, true_negative, false_positive, false_negative)
        precision[feminine_key] = self.precision(true_positive, false_positive)
        sensitivity[feminine_key] = self.sensitivity(true_positive, false_negative)
        
        accuracy[masculine_key] = self.accuracy(true_negative, true_positive, false_negative, false_positive)
        precision[masculine_key] = self.precision(true_negative, false_negative)
        sensitivity[masculine_key] = self.sensitivity(true_negative, false_positive)
        
        return { "accuracy": accuracy, "sensitivity": sensitivity, "precision": precision }


    def compare_assumption_with_reality(self, my_set):
        true_positive = 0
        true_negative = 0 
        false_positive = 0
        false_negative = 0

        # feminine -> positive 
        # masculine -> false

        for item in my_set:
            if item[gender_key] == masculine_char and item[assumption_key] == masculine_char:
                true_negative += 1

            if item[gender_key] == masculine_char and item[assumption_key] == feminine_char:
                false_negative += 1

            if item[gender_key] == feminine_char and item[assumption_key] == feminine_char:
                true_positive += 1

            if item[gender_key] == feminine_char and item[assumption_key] == masculine_char:
                false_positive += 1 
            
        return {
            "true_positive": true_positive,
            "true_negative": true_negative,
            "false_positive": false_positive,
            "false_negative": false_negative
        }


    def accuracy(self, true_positive, true_negative, false_positive, false_negative):
        acertos = true_positive + true_negative
        total = true_positive + true_negative + false_positive + false_negative
        return acertos / total


    def precision(self, true_positive, false_positive):
        return true_positive / (true_positive + false_positive)


    def sensitivity(self, true_positive, false_negative):
        return true_positive / (true_positive + false_negative)
    
    
    def get_assumption(self, ending_char, analysis_table):
        assumption = masculine_char
        
        if ending_char in analysis_table:
            char_probability_by_gender = analysis_table[ending_char]

            if log(char_probability_by_gender[feminine_key]) > log(char_probability_by_gender[masculine_key]):
                assumption = feminine_char

        return assumption

    def names_by_gender(self, names_list):
        analysis_table = self.get_ending_char_probabilities_by_gender(self.training_set)
        names_by_gender = {}
        
        for name in names_list:
            ending_char = name[-1:]
            
            if self.get_assumption(ending_char, analysis_table) == feminine_char:
                names_by_gender[name] = feminine_key
            else:
                names_by_gender[name] = masculine_key
                
        return names_by_gender
