"""
This file contains the second baseline. 
It marks tokens as an intensifier if they are 
in front of an adjective and if they are within 
a given list of intensifiers.
"""

#####################################
#   modules
#####################################
from _preproc import train_test
import numpy as np
from sklearn.metrics import classification_report

#####################################
#   functions
#####################################

def get_inputs(doc):
    """
        Function to extract the tokens and pos-tags 
        as input for the model from the test data.
        Input:
        1. doc (list)               :   List, that contains token and pos-tag 
                                        input from the test data.
        1. (token, postag) (tuple)  :   Tuple containing the token and the 
                                        pos-tag.
    """
    return [(token, postag) for (token, postag, label) in doc]
    
def get_labels(doc):
    """
        Function to extract the labels as goldlabels 
        for the model from the test data.
        Input:
        1. doc (list)   :   List, that contains token and pos-tag 
                            input from the test data.
        1. label (str)  :   String containing the label.
    """
    return [label for (token, postag, label) in doc]

def baseline_two(x_test):
    """
        Function for the second baseline.
        It marks tokens as an intensifier if they are in 
        front of an adjective and if they are within a given 
        list of intensifiers.
    """

    # list of predicted labels
    y_pred = list()

    # read in the file with the intensifiers
    with open("list_intensifiers.txt", "r", encoding="UTF-8-sig") as file:
        intensifiers = file.read()

    # look into a sentence
    for doc in x_test:
        sent_pred = list()
        # go through each token
        for i, token in enumerate(doc):
            if i < len(doc)-1:
                # if the following token is an adjective
                if doc[i+1][1] == "ADJA" or doc[i+1][1] == "ADJD":
                    # look if the token is within the list
                    # of intensifiers
                    if token[0] in intensifiers:
                        sent_pred.append("B-ITSF")
                    # if it is not, label it as O
                    else:
                        sent_pred.append("O")
                # if the following token is not an adjective
                # it is not an intensifier of an adjective
                # and therefore O
                else:
                    sent_pred.append("O")
            # if the last token is in the intensifier list
            else:
                sent_pred.append("O")

        y_pred.append(sent_pred)

    return y_pred

training_data, test_data = train_test()

x_test = [get_inputs(doc) for doc in test_data]

y_test = [get_labels(doc) for doc in test_data]

pred_baseline_two = baseline_two(x_test)
