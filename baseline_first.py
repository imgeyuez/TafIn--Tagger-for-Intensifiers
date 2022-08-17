"""
    This file contains the implementation of the first baseline
    which simply is the outcome of the SoMeWeTa tagger:
    https://github.com/tsproisl/SoMeWeTa 
    
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

def baseline_first(x_test):
    """
        First baseline model to label intensifiers of 
        adjectives. 
        Input:
        1. x_test (list)    :   List, that contains the sentences
                                of the test data.
        Output:
        1. y_pred (list)    :   List that contains the predicted 
                                likelihood labels for each token in 
                                every sentence.
    """
    # list in which the predicted labels will be stored in 
    y_pred = list()

    # for every document/sentence in the test set
    for doc in x_test:
        # list for the labels of a specific sentence
        sent_pred = list()

        # for every token within the sentence
        for index, token in enumerate(doc):
            # if token is marked as an intensifier
            if token[1] == "PTKIFG":
                # check, if token before is also one
                # if not, it is the beginning of an intensifier
                if doc[index-1] !="PTKIFG":
                    # append the predicted label to the labels of the 
                    # sentence
                    sent_pred.append("B-ITSF")
                # if yes, it is the continuation of an intensifier
                else:
                    # append the predicted label to the labels of the 
                    # sentence
                    sent_pred.append("I-ITSF")
            # if it is not marked as an intensifier, it is not
            # one 
            else:
                # append the predicted label to the labels of the 
                # sentence
                sent_pred.append("O")

        # append the predicted label for one sentence to the 
        # list of all predictions
        y_pred.append(sent_pred)

    return y_pred

# generating the data
training_data, test_data = train_test()

# generating the inputs for the testdata
x_test = [get_inputs(doc) for doc in test_data]


# extract the labels from the testdata
y_test = [get_labels(doc) for doc in test_data]

#pred_baseline_one = baseline_first(x_test)
