from _preproc import train_test

import pycrfsuite
import numpy as np
from sklearn.metrics import classification_report

training_data, test_data = train_test()

"""
So schaut die train data aus:
    [('Ich', 'PPER', 'O'), ('hab', 'VAFIN', 'O'), ('dann', 'ADV', 'O'), 
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

########## here starts the model ##########

def wordfeatures(doc, i):
    """
        example document:
        [('In', 'APPR', 'O'), ('einem', 'ART', 'O'), ('richtigen', 'ADJA', 'O'), 
        ('Restaurant', 'NN', 'O'), (',', '$,', 'O'), ('Freitagsabends', 'NN', 'O'), 
        ('.', '$.', 'O')]

        i want:
        - features for all words
    
    """
    token = doc[i][0]
    postag = doc[i][1]

    # features I want from all words 
    features = {
        "bias": 1.0,
        "token": token,
        "token.islower()": token.islower(), 
        "postag": postag,
    }

    # information I want starting from the second token
    if i > 0:
        prev_token = doc[i-1][0]
        prev_postag = doc[i-1][1]
        features.update({
            "prev_token": prev_token,
            "prev_postag": prev_postag,
            "prev_token.islower()": prev_token.islower(), 
            "prev_label": doc[i-1][2]
        })

    # if it is 0, it marks the beginning of a sentence
    else:
        features.update({"bos": True})
        
    # information I want until the last token 
    if i < len(doc)-1:
        next_token = doc[i+1][0]
        next_postag = doc[i+1][1]
        features.update({
            "next_token": next_token,
            "next_token.islower()": next_token.islower(),
            "next_postag": next_postag,
        })

    # if it is bigger, it marks the end of a sentence
    else:
        features.update({"eos": True})

    return features

# function for extracting features in documents
def extract_features(doc):
    return (wordfeatures(doc, i) for i in range(len(doc)))

# function fo generating the list of labels for each document
def get_labels(doc):
    return [label for (token, postag, label) in doc]
    
x_train = list()
for doc in training_data:
    x_train.append(extract_features(doc))

x_test = list()
for doc in test_data:
    x_test.append(extract_features(doc))

y_train = [get_labels(doc) for doc in training_data]

y_test = [get_labels(doc) for doc in test_data]

"""
    x_train für ein doc schaut aus wie: 
    [{'bias': 1.0, 'word': 'Es', 'word.islower()': False, 'postag': 'PPER', 'next_token': 'ist', 'next_token.islower()': True, 'next_postag': 'VAFIN'}, 
    {'bias': 1.0, 'word': 'ist', 'word.islower()': True, 'postag': 'VAFIN', 'prev_token': 'Es', 'prev_postag': 'PPER', 'next_token': 'sau', 'next_token.islower()': True, 'next_postag': 'ITJ'}, 
    {'bias': 1.0, 'word': 'sau', 'word.islower()': True, 'postag': 'ITJ', 'prev_token': 'ist', 'prev_postag': 'VAFIN', 'next_token': 'kalt', 'next_token.islower()': True, 'next_postag': 'ADJD'}, 
    {'bias': 1.0, 'word': 'kalt', 'word.islower()': True, 'postag': 'ADJD', 'prev_token': 'sau', 'prev_postag': 'ITJ', 'next_token': '.', 'next_token.islower()': False, 'next_postag': '$.'}, 
    {'bias': 1.0, 'word': '.', 'word.islower()': False, 'postag': '$.', 'prev_token': 'kalt', 'prev_postag': 'ADJD'}
    ]]
"""

# # training the model
trainer = pycrfsuite.Trainer(verbose=True)

# for each sequence of input and output within the input and output data
for xseq, yseq in zip(x_train, y_train):
    # train the model
    trainer.append(xseq, yseq)

# paramenters of the model
trainer.set_params({
    # coefficient for L1 penalty
    'c1': 0.5,

    # coefficient for L2 penalty
    'c2': 0.01,  

    # maximum number of iterations
    'max_iterations': 200,

    # whether to include transitions that
    # are possible, but not observed
    'feature.possible_transitions': True
    })

#print(trainer)

# Provide a file name as a parameter to the train function, such that
# the model will be saved to the file when training is finished
trainer.train("crf.model")

#print("crf.model")
# use the trained model
tagger = pycrfsuite.Tagger()
tagger.open("crf.model")
y_pred = [tagger.tag(xseq) for xseq in x_test]


# Create a mapping of labels to indices
labels = {"O": 0, "B-ITSF": 1, "I-ITSF": 2}

# Convert the sequences of tags into a 1-dimensional array
predictions = np.array([labels[tag] for row in y_pred for tag in row])
truths = np.array([labels[tag] for row in y_test for tag in row])

# Print out the classification report
print(classification_report(
    truths, predictions,
    target_names=["O", "B-ITSF", "I-ITSF"]))
