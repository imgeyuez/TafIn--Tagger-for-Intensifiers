"""
    This file contains various functions which are needed
    for the preprocessing of the used data.

    Every step is defined as a fuction and called within a 
    'bigger' function, which can be imported into the files
    that contain the baselines and models.

    Short explanation: 
        It will read the input of .tsv-files and will return
        two lists which contain the preprocessed inputs,
        splitted into train and test data.
    
    Quick overview of each function:
        readfile()      :   Reads the input of every .tsv-file 
                            within the folder.

        get_sentences() :   Generates sentences.

        pos_tagging()   :   Generates PoS-Tags to each token.

        split_compounds():  Splits adjectivecompounds.

        tag_compounds() :   Adds PoS-Tags to each element of the
                            splitted adjectivecompound.

        labeling()      :   Adds BIO-labeling.

        annotation()    :   Creates the finished annotations with
                            PoS-tag and label information.

        train_test()    :   Divides the data into train and test
                            data.

"""

#####################################
#   modules
#####################################

# import needed modules
import os, glob
import re
from someweta import ASPTagger
from charsplit import Splitter
from sklearn.model_selection import train_test_split

# load the model of the ASPTagger module
# module for the pos-tagging
model = "german_web_social_media_2020-05-28.model"
asptagger = ASPTagger()
asptagger.load(model)

#####################################
#   functions
#####################################

def readfile():
    """
        Reads in the input of every -tsv-file within the folder
        and saves its content within a variable.
        One row of the data is one element within the variable.
        Input:
        
        Output:
        1. files_data (list)        : List, that contains all the input
                                        from the .tsv-files.
                                        One element in the list is qual to
                                        one line in the file.
    """

    # list which will contain all the input
    files_data = list()

    # every .tsv-file in the folder ...
    for filename in glob.glob('*.tsv'):
        # ... will be opened and read
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode
            file_input = file.readlines()

            # add line to the list which will contain all data
            for line in file_input:
                files_data.append(line.split("\t"))
        

    return files_data

def get_sentences(file_data):
    """
        Gets all the listelements that contain a token and puts them 
        together into a sentence.
        Input:
        1. file_data (list) :   List, that contains all the input
                                from the .tsv-files.
                                One element in the list is qual to
                                one line in the file.
        Output:
        1. sentences (list) :   List, that contains all the input
                                in form of sentences.
                                One list element is a sentence as a
                                list, containing every token as an
                                element:
                                [['19-1', '1548-1550', 'Es', '_', '\n'], 
                                ['19-2', '1551-1556', 'ist', '_', '\n'], 
                                ['19-3', '1557-1566', 'saukalt', 'Intensifier', '\n'], 
                                ['19-4', '1567-1577', '.', '_', '\n']]
    """
    
    # list in which one sentence will be preserved
    sentence = []

    # list which will contain all the sentences in form of
    # sentences = [["One", "listelement", "is", "a", "sentence", "."],
    #             ["Containing", "all", "token", "."]]
    sentences = []

    lenght = len(file_data)

    # go through every line extracted from the files
    for index, element in enumerate(file_data):

        if index+1 == lenght:
            sentence.append(element)
            sentences.append(sentence)
            sentence = list()

        else:
            # every line which contais a token begins with this
            # pattern
            pattern = re.search(r"^([0-9]+-[0-9]+)", element[0])

            # if the pattern matches, append the line of the token
            # to the variable of ONE sentence
            if pattern:
                sentence.append(element)
            
            # if it does not match it marks the ending of
            # a sentence
            else:
                # if the element is not empty
                if sentence != []:
                    # append the sentence as an element within
                    # the list containing all the sentences
                    sentences.append(sentence)
                    # empty the list
                    sentence = list()

    return sentences

def pos_tagging(sentences):
    """
        Generates PoS-tags for all tokens.
        Input:
        1. sentences (list) :   List, that contains all the input
                                in form of sentences.
                                One list element is a sentence as a
                                list, containing every token as an
                                element.
        Output:
        1. tokens_tags (list):  List which contains of the sentences but
                                the tokens now consist of (token, PoS-tag)-pairs.
                                [[('token', 'tag'), ('token', 'tag')], 
                                [('token', 'tag'), ('token', 'tag')]]
    """

    # list, which will contain the tokens that need to be tagged 
    # within the sentences
    sentences_to_tag = list()


    for sentence in sentences:
        # list, which will contain all tokens of each sentence
        sent = list()

        for token in sentence:
            # extract the token from the data
            # form of token:
            # 1-6	35-45	gefälschte	_	
            sent.append(token[2])
        
        # if one sentence is finished, add the sentence, which
        # contains just the tokens, to the sentences_to_tag list
        sentences_to_tag.append(sent)

    # list, which will contain the token, tag pairs
    tokens_tags = list()

    for sentence in sentences_to_tag:
        sent_tagged = list()
        # tags every token of the sentence. for details see 
        # SoMeWeTa project: https://github.com/tsproisl/SoMeWeTa 
        tagged_sentence = asptagger.tag_sentence(sentence)
        for index, item in enumerate(tagged_sentence):
            sent_tagged.append(item)

        tokens_tags.append(sent_tagged)
        

    return tokens_tags

def split_compounds(sentences, tokens_tags):
    """
        Generates PoS-tags for all tokens.
        Input:
        1. sentences (list) :   List, that contains all the input
                                in form of sentences.
                                One list element is a sentence as a
                                list, containing every token as an
                                element.
        2. tokens_tags (list):  List which contains of the sentences but
                                the tokens consist of (token, PoS-tag)-pairs.
        Output:
        1. splitted_compounds
            (list)          :   List, that contains tuples with information
                                for sentence number, token number, token, and
                                the elements is has been splitted into, like:
                                (7, 2, 'saukalt', ['Sau', 'Kalt'])
                                for every compound.
    """

    # list, containing all the adjectivecompounds that need
    # to be splitted
    compounds = list()

    # for every sentence in sentences
    for index, sentence in enumerate(sentences):
        # for every token in the sentence
        for i, token in enumerate(sentence):
            # look, if the token is marked as an intensifier
            # aka not marked as "_"
            if token[-2] != "_":
                # if it is, look, if PoS-taf is an 
                # adjective --> predicative or attributive
                pos_tag = tokens_tags[index][i]
                if pos_tag[1] == "ADJD" or pos_tag[1] == "ADJA":
                    # if it is marked as such, it possibly is an
                    # adjectivecompound and therefore needs to be 
                    # splitted
                    compounds.append((index, i, token))

    # model for splitting
    # for details see: https://github.com/dtuggener/CharSplit 
    splitter = Splitter()
    """
        Form:
        [(0.1740327189765392, 'Zucker', 'Süß'), (-1.5975678869950305, 'Zuck', 'Ersüß'), (-2.1849865951742626, 'Zuc', 'Kersüß'), 
        (-3, 'Zucke', 'Rsüß')]  
    """
    # list that will contain the splitted compounds
    splitted_compounds = list()

    for compound in compounds:
        # form of compound:
        # (7, 2, ['19-3', '1557-1566', 'saukalt', 'Intensifier', '\n'])
        
        splitted_compound = splitter.split_compound(compound[2][2])
        # form of splitted_compound:
        # [(-0.5835459759340652, 'Wirk', 'Lich'), (-1.2466482494150914, 'Wir', 'Klich'), (-1.5259082915111741, 'Wirkl', 'Ich')] 
        # [(0.8513328138442754, 'Ein', 'Fach'), (-0.7000849466864454, 'Einf', 'Ach')]
        if splitted_compound[0][0] > 0:
            lexem1 = str(splitted_compound[0][1]).lower()
            lexem2 = str(splitted_compound[0][2]).lower()
            splitted_compounds.append((compound[0], compound[1], compound[2][2], [lexem1, lexem2]))

    return splitted_compounds

def tag_compounds(splitted_compounds):
    """
        Generates PoS-tags and label for the single elements 
        of the compound(s). 
        Input:
        1. splitted_compounds
            (list)          :   List, that contains tuples with information
                                for sentence number, token number, token, and
                                the elements is has been splitted into, like:
                                (7, 2, 'saukalt', ['Sau', 'Kalt'])
                                for every compound.
        Output:
        1. sent_tok_tag      
            (dict)          :   Dictionary, that contains the compound as keys, and 
                                the splitted compound elements as values while each
                                element is a tuple with the token, the pos-tag and
                                the label:
                                {'saukalt': (('sau', 'ITJ', 'B-ITSF'), 
                                ('kalt', 'ADJD', 'O'))}
    """

    # dictionary for the the PoS-tagged compounds
    sent_tok_tag = dict()

    # list_of_fail_annotated = list()

    # for every compound 
    for compound in splitted_compounds:
        # compound form:
        """
            (7, 2, 'saukalt', ['Sau', 'Kalt'])
        """
        # list for the token and tags
        tokens_tags = list()
        # tag the elements (see def pos_tagging)
        tagged_lexems = asptagger.tag_sentence(compound[-1])
        # append tagged element to the list 
        tokens_tags.append(tagged_lexems)

        """
        Elements in token_tags look like
            [('Sau', 'NN'), ('Kalt', 'ADJD')]

        Goal for the final annotation is:
        token, pos-tag, label, as in :
            sau,    NN,     B-ITSF
            kalt,   ADJD,   O
        
        So in general:
            sentence_id, token_id, [lex1, tag, BIO], [lex2, tag, BIO]
        """

        if tokens_tags[0][1][1] == "ADJD":
            sent_tok_tag[compound[2]] = (tokens_tags[0][0][0], tokens_tags[0][0][1], "B-ITSF"), (tokens_tags[0][1][0], tokens_tags[0][1][1], "O")

        elif tokens_tags[0][1][1] == "ADJA":
            sent_tok_tag[compound[2]] = (tokens_tags[0][0][0], tokens_tags[0][0][1], "B-ITSF"), (tokens_tags[0][1][0], tokens_tags[0][1][1], "O")

        # else:
        #     list_of_fail_annotated.append(compound)

    return sent_tok_tag

def labeling(sentences, tokens_tags):
    """
        Generates the BIO-annotation/labels for each token
        based on the previous annotation.
        BIO-Tagging:
        B-ITSF  --> Beginning of Intensifier
        I-ITSF --> Inside of Intensifier
        O       --> Outside of Intensifier
        Example on: Es ist ein bisschen kalt.
            Es          --> O
            ist         --> O
            ein         --> B-ITSF
            bisschen    --> I-ITSF
            kalt        --> O
            .           --> O

        Input:
        1. sentences (list) :   List, that contains all the input
                                in form of sentences.
                                One list element is a sentence as a
                                list, containing every token as an
                                element.
        2. tokens_tags (list):  List which contains of the sentences but
                                the tokens consist of 
                                (token, PoS-tag)-pairs.
        Output:
        1. label (list)     :   List that contains the labels for every
                                token within a sentence.
    """
    # list that will contain all labels
    label = list()

    # for every sentence in sentences
    for i, sentence in enumerate(sentences):
        # generate a list that will contain the labels
        # of the tokens within that sentence
        sent_labels = list()

        # list, in which a tag sequence will/can be stored
        itsf_seq = list()

        for index, token in enumerate(sentence):
            """
            token in form of:
                # ['18-3', '1557-1566', 'richtigen', '_', '\n']
                # ['18-2', '1551-1556', 'einem', '_', '\n']
            """
            # if token is not "_", it is marked as an intensifier
            if token[-2] != "_":
                
                # if "[" is not in the label of the token,
                # it is not part of a sequence of an intensifier
                if "[" not in token[-2]:
                    # and if the next token is also an ADJA or ADJD
                    # it is truly an intensifier of an adjective
                    if tokens_tags[i][index+1][1] == "ADJA" or tokens_tags[i][index+1][1] == "ADJD":
                        sent_labels.append("B-ITSF")

                    # if not, it is an intensifier of something else and 
                    # therefore not what we are looking for 
                    else:
                        sent_labels.append("O")

                # if "[" is within the label, it needs to be checked, if the 
                # token before it also has it.
                # if not, mark it as Beginning, if yes, mark it as Intern
                # we also need to check again if it is an intensifier of an adjective
                elif "[" in token[-2]:
            
                    # if the token before is also tagged with an [,
                    # it is in item within the sequence -> I tag
                    if "[" in sentence[index-1][-2]:
                        itsf_seq.append("I-ITSF")
                    # If the token before is not an *, and there fore an 
                    # Intensifier for itself or just no intensifier at all
                    # add it as a beginning to the sequence
                    elif "[" not in sentence[index-1][-2]:
                        itsf_seq.append("B-ITSF")

                    # check, if the next token is an Intensifier, 
                    # or if not, an adjective.
                    # if it is no intensifier, die sequence ended
                    # and if it is no adjective, the intensifier is
                    # not for an adjective 

            # is token not marked as intensifier
            elif token[-2] == "_": 
                
                # look, if the sequence list is filled
                if itsf_seq:
                 
                    # if there are labels, check, if token is an adjective
                    if tokens_tags[i][index][1] == "ADJA" or tokens_tags[i][index][1] == "ADJD":
                    #if token[-2] == "ADJA" or token[-2] == "ADJD":
                 
                        # if it is an adjective, the labels of the sequence
                        # of annotations can be added
                        # and also the annotation for the token itself
                        sent_labels.extend(itsf_seq)
                        itsf_seq = list() # leeren
                        sent_labels.append("O")
                 
                    # if it is not an adjective, the sequence of labels
                    # is not an intensifier for an adjective and
                    # therefore needs to be "replaced" with O's
                    else:
                        for itsf in itsf_seq:
                            sent_labels.append("O")
                        itsf_seq = list() #leeren
                        sent_labels.append("O")

                else:
                    sent_labels.append("O")
        
        label.append(sent_labels)
    
    return label  

def annotation(tokens_tags, labels):
    """
        Generates the final annotation for each token/sentence.
        Input:
        1. tokens_tags (list):  List which contains of the sentences but
                                the tokens consist of 
                                (token, PoS-tag)-pairs.
        2. labels (list)    :   List that contains the labels for every
                                token within a sentence.
        Output:
        1. documents (list) :   List, with each listelement being a list of
                                tokens of a sentence with the annotation:
                                (token, pos_tag, label)
    """
    # list that will contain all the sentences
    documents = list()

    # for every sentence
    for index, sentence in enumerate(tokens_tags):
        # generate a list, that will contain the annotation for that
        # very sentence
        sent_docs = list()
        # for every token-tag pair
        for i, token_tag in enumerate(sentence):
            # extract the token
            token = token_tag[0]
            # extract the pos-tag
            pos_tag = token_tag[1]
            # extract the label
            label = labels[index][i]

            # append them as one entry for the sentence
            sent_docs.append((token, pos_tag, label))
        
        # append the full annotated sentence to the 
        # variable that will contain all data
        documents.append(sent_docs)

    return documents

def train_test():
    """
        Function, that calls all the other functions
        in order to generate the needed data, puts everything
        (compounds and all) together and divides it into 
        train and test data. 
        Input:
        Output:
        1. training_data (list) :   List, that contains all the
                                    data that shall be used to
                                    train a model.
        2. test_data (list)     :   List, that contains all the
                                    data that shall be used to
                                    test a model.
    """
    file_data = readfile()
    #print(file_data)

    sentences = get_sentences(file_data)
    #print(sentences)

    tokens_tags = pos_tagging(sentences)
    #print(tokens_tags)

    splitted_compounds = split_compounds(sentences, tokens_tags)
    #print(splitted_compounds)

    tagged_compounds = tag_compounds(splitted_compounds)
    #print(tagged_compounds)

    # get keys of the dictionary
    keys = tagged_compounds.keys() 
    #print(keys)

    labels = labeling(sentences, tokens_tags)
    #print(labels)

    # annotated data without the splitted compounds
    work_annot = annotation(tokens_tags, labels)

    # documents which beholds each annotation for each token in a sentence
    # devided by sentences and with the splitted compounds
    documents = list()

    # adding the splitted compounds to the data
    for index, annot in enumerate(work_annot):
        document = list()
        for i, token in enumerate(annot):
            # if the token is within the dictionary,
            # it is an adjectivecompound and therefore
            # needs to be splitted into its elements
            if token[0] in keys:
                #print(token)
                tokens = tagged_compounds.get(token[0])
                document.append(tokens[0])
                document.append(tokens[1])

            else:
                document.append(token)
        
        documents.append(document)

    # use from sklearn the train_test_split function:
    # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    training_data, test_data = train_test_split(documents, test_size=0.2, shuffle=False)
    
    return training_data, test_data 
