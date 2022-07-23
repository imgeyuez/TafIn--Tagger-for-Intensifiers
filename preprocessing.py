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

    return file_input

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

def pos_tagging(sentences):
    from someweta import ASPTagger
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
