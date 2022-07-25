"""
    Thit file contains the steps for preprocessing
    the data. 
    The functions are:
    readfile()              : Reading in the file
    get_informations()      : Extracts the featurevec, gold_lables and sentences
    test_and_train_data()   : Divides data into train and test data
    pos_tagging()           : PoS-tags the data
"""

def readfile(filename):
    """
        Reads the file and saves its content within a variable.
        One row of the data is one entry within the list file_input
    """
    with open(filename, encoding="UTF-8-sig") as file:
        file_input = file.readlines()

    data_input = list()

    for input in file_input:
        data_input.append(input.split("\t"))

    return data_input

def generatesentences(data_input):
    # is needed for the pos-tagging
     # list which will contain all the sentences in form of
    # sentences = [["Ein", "Satz", "ist", "eine", "Liste", "von", "Tokens", "."],
    #             ["Zeitfliegen", "mögen", "einen", "Pfeil", "."]]
    sentences = []
    
    # list in which one sentence will be preserved
    sentence = []

    data_len = len(data_input)
    for index, data in enumerate(data_input):
        #if index == data_len-1:

        if data[0] != ".":
            sentence.append(data[0])
        else:
            sentence.append(data[0])
            sentences.append(sentence)
            sentence = list()

    return sentences

def train_test_data(data_input, sentences):
    
    train_data = list()
    test_data = list()

    train_sentences = list()
    test_sentences = list()
    
    data_amount = len(sentences)
    train_amount = data_amount / 100 * 80 #5,6

    token_number = 0

    for index, sentence in enumerate(sentences):
        if index <= train_amount:
            train_sentences.append(sentence)
            for token in sentence:
                train_data.append(data_input[token_number])
                token_number += 1

        else:
            test_sentences.append(sentence)
            for token in sentence:
                test_data.append(data_input[token_number])
                token_number += 1

    return train_data, test_data, train_sentences, test_sentences

# def pos_tagging(train_sentences, test_sentences):
#     from someweta import ASPTagger
#     """
#         This function uses the pretrained model someweta from empirist 
#         to tag the tokens which are within the sentences.
#     """

#     # loads pretrained model form someweta
#     model = "german_web_social_media_2020-05-28.model"

#     asptagger = ASPTagger()
#     asptagger.load(model)

#     # list in which the tokens with their tags will be saved in
#     # form: tuple(token, tag)
#     train_tokens_tags = list()

#     for sentence in train_sentences:
#         tagged_sentence = asptagger.tag_sentence(sentence)
#         for index in range(len(tagged_sentence)):
#             train_tokens_tags.append(tagged_sentence[index])

#     test_tokens_tags = list()

#     for sentence in test_sentences:
#         tagged_sentence = asptagger.tag_sentence(sentence)
#         for index in range(len(tagged_sentence)):
#             test_tokens_tags.append(tagged_sentence[index])

#     return train_tokens_tags, test_tokens_tags

def pos_tagging(sentences):
    from someweta import ASPTagger
    """
        This function uses the pretrained model someweta from empirist 
        to tag the tokens which are within the sentences.
    """

    # loads pretrained model form someweta
    model = "german_web_social_media_2020-05-28.model"

    asptagger = ASPTagger()
    asptagger.load(model)

    # list in which the tokens with their tags will be saved in
    # form: tuple(token, tag)
    tokens_tags = list()

    for sentence in sentences:
        tagged_sentence = asptagger.tag_sentence(sentence)
        for index in range(len(tagged_sentence)):
            tokens_tags.append(tagged_sentence[index])

    return tokens_tags
    
def splitcompounds(data_variable):

    compounds = list()

    for index, token in enumerate(data_variable):
        # if intensifier
        if token[-2] == "1":
            if token[1] == "ADJD" or token[1] == "ADJA":
                compounds.append([index, token])

    from charsplit import Splitter
    splitter = Splitter()

    """
        Form:
        [(0.1740327189765392, 'Zucker', 'Süß'), (-1.5975678869950305, 'Zuck', 'Ersüß'), (-2.1849865951742626, 'Zuc', 'Kersüß'), 
        (-3, 'Zucke', 'Rsüß')]  
    """
    #splitted_compounds = dict()
    splitted_compounds = list()

    for compound in compounds:
        # form of compound:
        # compund = [67, ['klitzeklein', 'ADJD', '0', 'None', '1', '\n']] 
        
        # form of splitted_compound = 
        # [[63, 'schweineschwer', ['Schweine', 'Schwer']], [67, 'klitzeklein', ['Klitze', 'Klein']]]
        splitted_compound = splitter.split_compound(compound[1][0])
        lexem1 = splitted_compound[0][1]
        lexem2 = splitted_compound[0][2]
        #splitted_compounds[compound[0]] = compound[1][0], [lexem1, lexem2]
        splitted_compounds.append([compound[0], compound[1][0], [lexem1, lexem2]])


    return compounds, splitted_compounds

def insert_compounds(data_variable, splitted_compounds):
    
    # hier token noch einmal pos-taggen und annotationen
    # ergänzen und dann
    # als compound elemente einfügen 
    # data in which compounds are splitted
    from someweta import ASPTagger

    model = "german_web_social_media_2020-05-28.model"
    asptagger = ASPTagger()
    asptagger.load(model)


    # [[63, 'schweineschwer', ['Schweine', 'Schwer']], 
    # [67, 'klitzeklein', ['Klitze', 'Klein']]]

    # create their pos-tag and annotation
    index_token_tag = dict()

    list_of_fail_annotated = list()

    for compound in splitted_compounds:
        
        tokens_tags = list()
        tagged_lexems = asptagger.tag_sentence(compound[2])
        tokens_tags.append(tagged_lexems)
      
        # in tokens_tags ist dann die form:
        # [[('Schweine', 'NN'), ('Schwer', 'ADJD')]]
        #print(tokens_tags)

        # Das will ich haben:
        # schweine, NN, 1, pred, 1          # später müsste hier ergänzt werden, ob es sem. steigerbar ist lol
        # schwer,   ADJD, 0, None, 0

        # will die form: [index, [[lex1, tag, ifoA, ped/att/None, itsf], [lex2, tag, ifoA, ped/att/None, itsf]]]

        if tokens_tags[0][1][1] == "ADJD":
            index_token_tag[compound[0]] = [tokens_tags[0][0][0], tokens_tags[0][0][1], "1", "pred", "1"], [tokens_tags[0][1][0], tokens_tags[0][1][1], "0", "None", "0"]

        elif tokens_tags[1][1][1] == "ADJA":
            index_token_tag[compound[0]] = [tokens_tags[0][0][0], tokens_tags[0][0][1], "1", "att", "1"], [tokens_tags[0][1][0], tokens_tags[0][1][1], "0", "None", "0"]

        else:
            list_of_fail_annotated.append(compound)


    #print(index_token_tag)
    # das ist das ergebnis:

    # {63: (['Schweine', 'NN', '1', 'pred', '1'], ['Schwer', 'ADJD', '0', 'None', '0']), 
    # 67: (['Klitze', 'NN', '1', 'pred', '1'], ['Klein', 'ADJD', '0', 'None', '0'])}

    new_data = list()
    keys = index_token_tag.keys() 

    for index, token in enumerate(data_variable):
        # wenn der index ein Kompositum ist,
        if index in keys:
        # werden anstelle des Kompositums
        # die beiden Lexeme eingetragen
            tokens = index_token_tag.get(index)
            new_data.append(tokens[0])
            new_data.append(tokens[1])

        # ist das Token bei dem Index kein 
        # Kompositum, können die Daten einfach
        # übernommen werden 
        else:
            new_data.append(token)

    return new_data


### RUN SCRIPT ###
def run_script(filename):

    data_input = readfile(filename)

    sentences = generatesentences(data_input)

    #print(train_test_data(data_input, sentences))
    train_data, test_data, train_sentences, test_sentences = train_test_data(data_input, sentences)
    #print(train_data)
    #print(test_data)
    #print(test_sentences)
    #print(train_sentences)
    
    #train_tokens_tags, test_tokens_tags = pos_tagging(train_sentences, test_sentences)
    #print(test_tokens_tags)
    train_tokens_tags = pos_tagging(train_sentences)
    test_tokens_tags = pos_tagging(test_sentences)

    # update the train_data
    for index, token in enumerate(train_data):
        pos_tag = train_tokens_tags[index][1]
        token.insert(1, pos_tag)

    # update the test_data
    for index, token in enumerate(test_data):
        pos_tag = test_tokens_tags[index][1]
        token.insert(1, pos_tag)

    compounds, train_splitted_compounds = splitcompounds(train_data)
    compounds, test_splitted_compounds = splitcompounds(test_data)


    new_train_data = insert_compounds(train_data, train_splitted_compounds)
    print(new_train_data)

if __name__ == "__main__":

    filename = "preproc_test.txt"

    run_script(filename)
