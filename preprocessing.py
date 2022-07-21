"""
    This file is for the preprocessing of the data.
    Good thing is that the data is already tokenized.
    That will be helpful.
    Results are supposed to be:D.h.:
    > PoS-Tagged Tokens
    > Splitting adjectivecompounds that were annotated as intensifiers

    So to be able to use this preprocessing file unproblematicly,
    the data has to be already tokenized.
"""

### To Do ###
# split adjective compounds that are marked as intensifiers
# add comments 
# extract if intensifier or no in seperate list ?

# module for PoS-Tagging
from someweta import ASPTagger

# import first baseline 
from baseline_first import baseline_first

### PREPROCESSING  ###

def readfile(filename):
    """
        Reads the file and saves its content within a variable.
        One row of the data is one entry within the list file_input
    """
    with open(filename, encoding="UTF-8-sig") as file:
        file_input = file.readlines()

    return file_input

def get_information(file_input):
    """
        This function will generate sentences out of the tokens.
        Because the data is already tokenized, the dot can 
        simply be used as a sentence-end marker.
    """

    # list in which one sentence will be preserved
    sentence = []
    # list which will contain all the sentences in form of
    # sentences = [["Ein", "Satz", "ist", "eine", "Liste", "von", "Tokens", "."],
    #             ["Zeitfliegen", "mögen", "einen", "Pfeil", "."]]
    sentences = []

    token_information = list()

    y_gold = list ()

    # go through the input from the file
    for i in range(len(file_input)):

        # ...split the input...
        content = file_input[i].split("\t")
        token_information.append(content)
        y_gold.append(content[-2])
        # extract the token
        token = content[0]
        # append the token to generate the one sentence
        sentence.append(token)

        if token == ".":
            sentences.append(sentence)
            sentence = []

    return token_information, sentences, y_gold


def features_and_labels(token_information):
    """ 
        Unterteilung von Train und Testdata 
        Sowie die jeweilige Selektierung der FEatures und Labels
    """
    train_features = list()
    train_gold = list()
    test_features = list()
    test_gold = list()
    number_data = len(token_information)
    train_data_len = number_data/100*80
    for index, data in enumerate(token_information):
        if index <= train_data_len:
            train_features.append(token_information[1],token_information[2])
            train_gold.append(token_information[3])
        else:
            test_features.append(token_information[1],token_information[2])
            test_gold.append(token_information[3])

    return train_features, train_gold, test_features, test_gold


def pos_tagging(sentences):
    
    """
        This function uses the pretrained model someweta from empirist 
        to tag the tokens which are within the sentences."""

    # loads pretrained model form someweta
    model = "german_web_social_media_2020-05-28.model"

    asptagger = ASPTagger()
    asptagger.load(model)

    # list in which the tokens with their tags will be saved in
    # form: tuple(token, tag)
    tagged_tokens = list()

    for sentence in sentences:
        tagged_sentence = asptagger.tag_sentence(sentence)
        for index in range(len(tagged_sentence)):
            tagged_tokens.append(tagged_sentence[index])
    
    return tagged_tokens


### SECOND BASELINE ###
def baseline_second(tagged_tokens):
    """
    hier ist noch ein Denkfehler, der ausgeglichen werden muss
    token muss ja nciht v sein, das davor muss n v sein, oder ein .
    sie ist voll cool.
    gar nicht 
    like this 
    
    """
    intensifier_pred = list()
    for index, token in enumerate(tagged_tokens):
        try:
            # if token in front of adjective:
            if tagged_tokens[index+1][1] == "ADJD" or tagged_tokens[index+1][1] == "ADJA":
                #check, if is a verb
                if tagged_tokens[index][1][0] == "V":
                    intensifier_pred.append(0)
                else:
                    intensifier_pred.append(1)
            else:
                intensifier_pred.append(0)
        except:
            intensifier_pred.append(0)

    return intensifier_pred

### TAFIN   ###

### RUN SCRIPT ###
def run_script(filename):
    file_input = readfile(filename)
    token_information, sentences, y_gold = get_information(file_input)
    #print(len(y_gold))
    tagged_tokens = pos_tagging(sentences)
    #print(tagged_tokens)
    intens_pred_first = baseline_first(tagged_tokens)
    #print(intens_pred_first)
    for pred, gold in zip(intens_pred_first, y_gold):
        if int(pred) != int(gold):
            print(pred, "\t", gold)
    print("FEDDIG")

if __name__ == "__main__":

    filename = "test_on_data5.txt"

    run_script(filename)
