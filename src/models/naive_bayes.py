import os
import pandas as pd
from unicodedata import normalize

feminine = "F"
masculine = "M"

class NaiveBayes(object):

    def __init__(self):
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'public'))

    def prob_bayes(self, my_set):
        char_set = ["a", "e", "o"]
        characteristics_dict = {}
        for char in char_set:
            characteristics_dict[char] = 0

        masculine_names_ending_in = characteristics_dict.copy()
        feminine_names_ending_in = characteristics_dict.copy()

        for item in my_set:
            item_name_ending_char = normalize("NFKD", item["Nome"][-1:]).encode("ASCII","ignore").decode("ASCII")
            item_gender = item["Gênero"]

            if item_name_ending_char in characteristics_dict:
                if item_gender == feminine:
                    feminine_names_ending_in[item_name_ending_char] += 1
                elif item_gender == masculine:
                    masculine_names_ending_in[item_name_ending_char] += 1

        num_of_feminine = len([item for item in my_set if item["Gênero"] == feminine])
        num_of_masculine = len([item for item in my_set if item["Gênero"] == masculine])

        analysis_table = []

        for char in char_set:
            curr_feminine_prob = (feminine_names_ending_in[char] / num_of_feminine) or 1
            curr_masculine_prob = (masculine_names_ending_in[char] / num_of_masculine) or 1

            analysis_table.append({
                "Final": char,
                "Feminino": curr_feminine_prob,
                "Masculino": curr_masculine_prob
            })

        return analysis_table

    def get_analysis_table(self):
        df = pd.read_csv(os.path.join(self.file_path, "nomes.csv"))

        names = df.to_dict("records")

        training_test_divisor = int(len(names)*0.64)
        test_validation_divisor = int(training_test_divisor + len(names)*0.18)

        training_set = names[:training_test_divisor]
        # testing_set = names[training_test_divisor:test_validation_divisor]
        # validation_set = names[test_validation_divisor:]

        return self.prob_bayes(training_set)

