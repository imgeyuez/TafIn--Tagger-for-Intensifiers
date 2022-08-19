"""
    This file contains the function needed for an
    evaluation.
"""
import numpy as np
from sklearn.metrics import classification_report

def evaluation(y_test, y_pred):
    """
        Evaluates a model based on the predicted labels.
        Input:
        1. y_test (list)    :   List of goldlabels for a 
                                specific testdata.
        2. y_pred (list)    :   List of predicted labels
                                for the same specific 
                                testdata.
        Output:
        None. It prints the results. 
    """

    # Create a mapping of labels to indices
    labels = {"O": 0, "B-ITSF": 1, "I-ITSF": 2}
  
    # Convert the sequences of tags into a 1-dimensional array
    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in y_test for tag in row])

    # Print out the classification report
    print(classification_report(
        truths, predictions,
        target_names=["O", "B-ITSF", "I-ITSF"]))
