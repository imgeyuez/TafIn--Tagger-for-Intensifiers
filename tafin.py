from _clean import readfile
from _clean import get_sentences
from _clean import pos_tagging
from _clean import split_compounds
from _clean import tag_compounds
from _clean import labeling
from _clean import annotation
from _clean_2 import test_and_train

import pycrfsuite
from sklearn.model_selection import train_test_split

filename = "0_test_data.txt"

file_data = readfile(filename)
sentences = get_sentences(file_data)
tokens_tags = pos_tagging(sentences)
splitted_compounds = split_compounds(sentences, tokens_tags)
tagged_compounds = tag_compounds(sentences, splitted_compounds)
keys = tagged_compounds.keys() 
labels = labeling(sentences, tokens_tags)
work_annot = annotation(tokens_tags, labels)
documents = list()
for index, annot in enumerate(work_annot):
        document = list()
        for i, token in enumerate(annot):
            if token[0] in keys:
                #print(token)
                tokens = tagged_compounds.get(token[0])
                document.append(tokens[0])
                document.append(tokens[1])

            else:
                document.append(token)
        
        documents.append(document )

#train_data, test_data = test_and_train(documents)

#print(train_data)  
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
        "word": token,
        "word.islower()": token.islower(), 
        #'word.lower()': token.lower(),
        #'word[-3:]': token[-3:],
        #'word[-2:]': token[-2:],
        #'word.isupper()': token.isupper(),
        #'word.istitle()': token.istitle(),
        #"in_list":token in...?,
        #"word.isdigit()": token.isdigit(),
        "postag": postag,
        #'postag[:2]': pos_tag[:2],
    }

    # information I want starting from the second token
    if i > 0:
        prev_token = doc[i-1][0]
        prev_postag = doc[i-1][1]
        features.update({
            "prev_token": prev_token,
            #"in_list":token in...?,
            #"prev_isdigit()": prev_token.isdigit(),
            "prev_postag": prev_postag,
            #"prev_label":???
        })

    # information I want until the last token 
    if i < len(doc)-1:
        next_token = doc[i+1][0]
        next_postag = doc[i+1][1]
        features.update({
            "next_token": next_token,
            "next_token.islower()": next_token.islower(),
            #"in_list":token in...?,
            #"next_isdigit()": next_token.isdigit(),
            "next_postag": next_postag,
        })

    return features

# function for extracting features in documents
def extract_features(doc):
    return [wordfeatures(doc, i) for i in range(len(doc))]

# function fo generating the list of labels for each document
def get_labels(doc):
    return [label for (token, postag, label) in doc]
    

x_inputs = [extract_features(doc) for doc in documents]
y_outputs = [get_labels(doc) for doc in documents]


x_train, x_test, y_train, y_test = train_test_split(x_inputs, y_outputs, test_size=0.2)
#print(x_train)
