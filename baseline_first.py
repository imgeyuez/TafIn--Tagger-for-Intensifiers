"""
    The first baseline will be the grouptag for intensifier,
    focus- and gradparticel from the someweta module itself. 

    Therefore the baseline is nothing but the def pos_tagging(sentences)
    where the tokens tagged with ... will be marked as intensifiers.
"""
from _preproc import train_test
import numpy as np
from sklearn.metrics import classification_report

training_data, test_data = train_test()

def get_inputs(doc):
    return [(token, postag) for (token, postag, label) in doc]
    
x_test = [get_inputs(doc) for doc in test_data]

def get_labels(doc):
    return [label for (token, postag, label) in doc]

y_test = [get_labels(doc) for doc in test_data]


def baseline_first(x_test):
    y_pred = list()

    for doc in x_test:
        sent_pred = list()

        for index, token in enumerate(doc):
            # if token is marked as an intensifier
            if token[1] == "PTKIFG":
                # check, if token before is also one
                # if not, it is the beginning of an intensifier
                # if yes, it is the continuation of an intensifier
                if doc[index-1] !="PTKIFG":
                    sent_pred.append("B-ITSF")
                else:
                    sent_pred.append("I-ITSF")
            else:
                sent_pred.append("O")

        y_pred.append(sent_pred)

    return y_pred

pred_baseline_one = baseline_first(x_test)

# Create a mapping of labels to indices
labels = {"O": 0, "B-ITSF": 1, "I-ITSF": 2}

# Convert the sequences of tags into a 1-dimensional array
predictions = np.array([labels[tag] for row in pred_baseline_one for tag in row])
truths = np.array([labels[tag] for row in y_test for tag in row])

# Print out the classification report
print(classification_report(
    truths, predictions,
    target_names=["O", "B-ITSF", "I-ITSF"]))
