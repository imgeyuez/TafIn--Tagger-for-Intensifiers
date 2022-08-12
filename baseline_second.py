"""
Das folgende Programm präsentiert die zweite Baseline.
Baselines werden verwendet, um vergleichen zu können, ob sich das 
implementierte Programm "lohnt" oder keinen Unterschied zu vorherigen
Methoden macht.

Die 1. Baseline: 
    POS-Tags ADJD & ADJA herausfiltern und das links davon
    stehende Element als Intensivierer markieren, solange es kein 
    Verb ist
    Also sprich: einfach eine heuristische Methode

Die 2. Baseline:
    Kann ein Modell von dem Empirist Modell darstellen mit ihrer 
    Sammelklasse von Fokus- Graduierungs- und Intensitätspartikeln. 
    Das von someweta

Könnte auch ne 3. Baseline einbauen, bei der mit den Wörterlisten
nach weiteren Intensivierern geschaut wird, aber weiß nicht, inwieweit
das schon zu viel wäre .. hmm
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


def baseline_two(x_test):

    # list of predicted labels
    y_pred = list()

    """
    So schaut die train data aus:
    [[('Ich', 'PPER', 'O'), ('hab', 'VAFIN', 'O'), ('dann', 'ADV', 'O'), 
    ('auch', 'ADV', 'O'), ('schnell', 'ADJD', 'O'), ('gewählt', 'VVPP', 'O'), 
    ('und', 'KON', 'O'), ('saß', 'VVFIN', 'O'), ('mit', 'APPR', 'O'), 
    ('meiner', 'PPOSAT', 'O'), ('sehr', 'PTKIFG', 'B-ITSF'), 
    ('aufgeräumten', 'ADJA', 'O'), (',', '$,', 'O'), ('gut', 'ADJD', 'O'), 
    ('gelaunten', 'ADJA', 'O'), ('und', 'KON', 'O'), ('gesprächigen', 'ADJA', 'O'), 
    ('Tochter', 'NN', 'O'), ('beim', 'APPRART', 'O'), ('Essen', 'NN', 'O'), 
    ('.', '$.', 'O')], [('WIR', 'PPER', 'O'), ('SIND', 'VAFIN', 'O'), 
    ('ZUSAMMEN', 'ADV', 'O'), ('ESSEN', 'NN', 'O'), ('GEGANGEN', 'VVPP', 'O'), 
    ('.', '$.', 'O')], [('In', 'APPR', 'O'), ('einem', 'ART', 'O'), 
    ('richtigen', 'ADJA', 'O'), ('Restaurant', 'NN', 'O'), (',', '$,', 'O'), 
    ('Freitagsabends', 'NN', 'O'), ('.', '$.', 'O')]]
    """

    # read in the file with the intensifiers
    with open("list_intensifiers.txt", "r", encoding="UTF-8-sig") as file:
        intensifiers = file.read()
            
    #print(intensifiers_list)

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

#baseline_two(x_test)
pred_baseline_two = baseline_two(x_test)

# for index, row in enumerate(pred_baseline_two):
#     for i, tag in enumerate(row):
#         print(tag, "\t", y_test[index][i])


# Create a mapping of labels to indices
labels = {"O": 0, "B-ITSF": 1, "I-ITSF": 2}

# Convert the sequences of tags into a 1-dimensional array
predictions = np.array([labels[tag] for row in pred_baseline_two for tag in row])
truths = np.array([labels[tag] for row in y_test for tag in row])

# Print out the classification report
print(classification_report(
    truths, predictions,
    target_names=["O", "B-ITSF", "I-ITSF"]))
