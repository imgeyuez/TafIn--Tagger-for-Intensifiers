from _clean import readfile
from _clean import get_sentences
from _clean import pos_tagging
from _clean import split_compounds
from _clean import tag_compounds
from _clean import labeling
from _clean import annotation
from _clean_2 import test_and_train

from sklearn.model_selection import train_test_split
import pycrfsuite

#filename = "0_test_data.txt"
filename = "8997_blog.xml.tsv"

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


x_train, x_test, y_train, y_test = train_test_split(x_inputs, y_outputs, test_size=0.2, shuffle=False)
#print(x_train)
"""
    x_train für ein doc schaut aus wie: 
    [{'bias': 1.0, 'word': 'Es', 'word.islower()': False, 'postag': 'PPER', 'next_token': 'ist', 'next_token.islower()': True, 'next_postag': 'VAFIN'}, {'bias': 1.0, 'word': 'ist', 'word.islower()': True, 'postag': 'VAFIN', 'prev_token': 'Es', 'prev_postag': 'PPER', 'next_token': 'sau', 'next_token.islower()': True, 'next_postag': 'ITJ'}, 
    {'bias': 1.0, 'word': 'sau', 'word.islower()': True, 'postag': 'ITJ', 'prev_token': 'ist', 'prev_postag': 'VAFIN', 'next_token': 'kalt', 'next_token.islower()': True, 'next_postag': 'ADJD'}, 
    {'bias': 1.0, 'word': 'kalt', 'word.islower()': True, 'postag': 'ADJD', 'prev_token': 'sau', 'prev_postag': 'ITJ', 'next_token': '.', 'next_token.islower()': False, 'next_postag': '$.'}, 
    {'bias': 1.0, 'word': '.', 'word.islower()': False, 'postag': '$.', 'prev_token': 'kalt', 'prev_postag': 'ADJD'}
    ]]
"""

"""     Ich glaube, das brauche ich nicht mehr

# # extrahierung der trainings features und labels
# x_train = [extract_features(doc) for doc in train_data]
# y_train = [get_lables(doc) for doc in train_data]

# # extrahierung der test features und labels
# x_test = [extract_features(doc) for doc in test_data]
# y_test = [get_lables(doc) for doc in test_data]
# """

# # training the model
trainer = pycrfsuite.Trainer(verbose=True)

# for each sequence of input and output within the input and output data
for xseq, yseq in zip(x_train, y_train):
    # train the model
    trainer.append(xseq, yseq)

# paramenters of the model
trainer.set_params({
    # coefficient for L1 penalty
    'c1': 0.1,

    # coefficient for L2 penalty
    'c2': 0.01,  

    # maximum number of iterations
    'max_iterations': 200,

    # whether to include transitions that
    # are possible, but not observed
    'feature.possible_transitions': True
    })

# Provide a file name as a parameter to the train function, such that
# the model will be saved to the file when training is finished
trainer.train("crf.model")


# use the trained model
tagger = pycrfsuite.Tagger()
tagger.open("crf.model")
y_pred = [tagger.tag(xseq) for xseq in x_test]

print(y_pred)
print("\n")
print(y_test)
