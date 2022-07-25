"""
    This file contains the steps for preprocessing
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

    return file_input

def generatesentences(file_input):
    # is needed for the pos-tagging
     # list which will contain all the sentences in form of
    # sentences = [["Ein", "Satz", "ist", "eine", "Liste", "von", "Tokens", "."],
    #             ["Zeitfliegen", "mögen", "einen", "Pfeil", "."]]
    sentences = []
    
    # list in which one sentence will be preserved
    sentence = []

    data_len = len(file_input)
    for index, token in enumerate(file_input):
        #if index == data_len-1:
        token_content = token.split("\t")

        if token_content[0] != ".":
            sentence.append(token_content[0])
        else:
            sentence.append(token_content[0])
            sentences.append(sentence)
            sentence = list()

    return sentences

def pos_tagging(file_input, sentences):
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
    
    # adding PoS-Information to the data in a new datafile
    new_data = list()

    for index, token in enumerate(file_input):
        content = token.split("\t")
        pos_tag = tokens_tags[index][1]
        content.insert(1, pos_tag)
        new_data.append(content)
    
    return new_data

def splitcompounds(new_data):

    compounds = list()

    for index, token in enumerate(new_data):
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

    # doch lieber in dictionary umwandeln?? 
    splittet_compounds = list()

    for compound in compounds:
        # form of compound:
        # compund = [67, ['klitzeklein', 'ADJD', '0', 'None', '1', '\n']] 

        splitted_compound = splitter.split_compound(compound[1][0])
        lexem1 = splitted_compound[0][1]
        lexem2 = splitted_compound[0][2]
        splittet_compounds.append([compound[1][0], [lexem1, lexem2]])

    return compounds, splittet_compounds

def insert_compounds(new_data, compounds, splittet_compounds):

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
    index_token_tag = list()
    compound_index = list()

    for compound in splitted_compounds:
        annot = list()
        #print(compound[0])
        compound_index.append(compound[0])
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
            annot.append([tokens_tags[0][0][0], tokens_tags[0][0][1], "1", "pred", "1"])
        elif tokens_tags[1][1][1] == "ADJA":
            annot.append([tokens_tags[0][0][0], tokens_tags[0][0][1], "1", "att", "1"])

        annot.append([tokens_tags[0][1][0], tokens_tags[0][1][1], "0", "None", "0"])
    
        index_token_tag.append([compound[0], annot])

    # das ist das ergebnis:
    #[[63, [['Schweine', 'NN', '1', 'pred', '1'], ['Schwer', 'ADJD', '0', 'None', '0']]], 
    # [67, [['Klitze', 'NN', '1', 'pred', '1'], ['Klein', 'ADJD', '0', 'None', '0']]]]
    
    
    new_new_data = list()

    #print(compound_index)
    for index, token in enumerate(new_data):
        if index in compound_index:
            new_new_data.append()
        else:
            new_new_data.append(token)

def get_informations(file_input):
    """
        Maingoal of this function is to extract the specific
        information of each inputline. 
        Extracted will be: 
            inputvectors: Inputvectors (Feature1, Feature2, Feature3)
                Feature 1   : Is token in front of an adjective? (ifoa)
                Feature 2   : Is the adjective predicative or attributive?
                Feature 3   : Is the adcetive semantically graduable?  # still needs to be added in annotation
            
            gold_labels : The annotation if token is intensifier or not
            sentences   : Sentences markend by the token "." (possible, because
                            the data is already tokenized)

    """

    # list which will contain all the sentences in form of
    # sentences = [["Ein", "Satz", "ist", "eine", "Liste", "von", "Tokens", "."],
    #             ["Zeitfliegen", "mögen", "einen", "Pfeil", "."]]
    sentences = []
    
    # list in which one sentence will be preserved
    sentence = []

    # features
    # feature1 = list()
    # feature2 = list()
    # feature3 = list()

    featurevec = list()

    # gold lables
    gold_lables = list()

    # go through the input from the file
    for index, item in enumerate(file_input):
        # ...split the input...
        content = item.split("\t")

        # extract feature1
        # feature1.append(content[1])
        # # extract feature2
        # feature2.append(content[2])
        # extract feature3 # still needs to be added
        # feature3 = content[3]

        feature1 = content[1]

        # für Naive Bayes gaussisch müssen alles Zahlen sein, therefore
        if content[2] == "pred":
            feature2 = 1
        elif content[2] == "att":
            feature2 = 2
        elif content[2] == "None":
            feature2 = 0
        #feature2 = content[2]

        featurevec.append((feature1, feature2))

        gold_lables.append(content[3]) # later on element 4, if feature3 is added
        # gold_lables.append(content[4])

        # generate a sentence for the pos-tagging
        sentence.append(content[0])

        if content[0] == ".":
            sentences.append(sentence)
            sentence = list()

    # inputvectors
    #inputvectors = zip(feature1, feature2) # add feature3 later on
    #inputvectors = zip(feature1, feature2, feature3)

    return featurevec, gold_lables, sentences

def test_and_train_data(featurevec, gold_lables):
    """"
        This function divides the data in 
        train and test data.
    """
    data_amount = len(featurevec)
    train_amount = data_amount / 100 * 80

    train_features = list()
    train_lables = list()

    test_features = list()
    test_lables = list()

    for index, (input, gold) in enumerate(zip(featurevec, gold_lables)):

        if index <= train_amount:
            train_features.append(input)
            train_lables.append(gold)

        else:
            test_features.append(input)
            test_lables.append(gold)


    return train_features, train_lables, test_features, test_lables
