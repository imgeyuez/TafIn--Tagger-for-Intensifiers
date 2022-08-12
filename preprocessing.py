import os, glob
import re
from someweta import ASPTagger
from charsplit import Splitter
from sklearn.model_selection import train_test_split

# load the modules

# module for the pos-tagging
model = "german_web_social_media_2020-05-28.model"
asptagger = ASPTagger()
asptagger.load(model)

def readfile():
    """
        Reads the file and saves its content within a variable.
        One row of the data is one entry within the list file_input
    """

    files_data = list()

    for filename in glob.glob('*.tsv'):
        with open(os.path.join(os.getcwd(), filename), 'r', encoding="UTF-8-sig") as file: # open in readonly mode
            file_input = file.readlines()
            for line in file_input:
                files_data.append(line.split("\t"))
            
    """
    files_data = list()

    for filename in filenames:
        with open(filename, 'r', encoding="UTF-8-sig") as file:
            file_input = file.readlines()


            for line in file_input:
                files_data.append(line.split("\t"))
    """

    return files_data

def get_sentences(file_data):
    """
        This function will get all the rows within the data that behold
        a token.
    """
    # list in which one sentence will be preserved
    sentence = []
    # list which will contain all the sentences in form of
    # sentences = [["Ein", "Satz", "ist", "eine", "Liste", "von", "Tokens", "."],
    #             ["Zeitfliegen", "mögen", "einen", "Pfeil", "."]]
    sentences = []

    lenght = len(file_data)

    # go through the input from the file
    for index, element in enumerate(file_data):
        if index+1 == lenght:
            sentence.append(element)
            sentences.append(sentence)
            sentence = list()

        else:
            #pattern = re.search(r"^([0-9]+-[0-9]+)", element[0])
            pattern = re.search(r"^([0-9]+-[0-9]+)", element[0])

            if pattern:
                sentence.append(element)
            
            else:
                if sentence != []:
                    sentences.append(sentence)
                    sentence = list()

    return sentences

def pos_tagging(sentences):

    sentences_to_tag = list()

    for sentence in sentences:
        sent = list()

        for token in sentence:
            # print(token)
            # print(token[2])
            sent.append(token[2])
        
        sentences_to_tag.append(sent)

    tokens_tags = list()

    for sentence in sentences_to_tag:
        sent_tagged = list()
        tagged_sentence = asptagger.tag_sentence(sentence)
        for index, item in enumerate(tagged_sentence):
            sent_tagged.append(item)

        tokens_tags.append(sent_tagged)
        

    return tokens_tags

def split_compounds(sentences, tokens_tags):
    compounds = list()

    for index, sentence in enumerate(sentences):
        #sentence schauen aus wie 
        """
            [['19-1', '1548-1550', 'Es', '_', '\n'], 
            ['19-2', '1551-1556', 'ist', '_', '\n'], 
            ['19-3', '1557-1566', 'saukalt', 'Intensifier', '\n'], 
            ['19-4', '1567-1577', '.', '_', '\n']]
        """

        for i, token in enumerate(sentence):
            # token sehen so aus:
            """
                ['19-1', '1548-1550', 'Es', '_', '\n']
                ['19-2', '1551-1556', 'ist', '_', '\n']
                ['19-3', '1557-1566', 'saukalt', 'Intensifier', '\n']    
                ['19-4', '1567-1577', '.', '_', '\n']
            """
            
            # wenn token als intensivierer markiert ist
            if token[-2] != "_":
                # pos-tag ansehen, ob es ein adjektiv ist
                # so sehen pos_tag aus:
                """
                    ('bisschen', 'PIS')
                    ('saukalt', 'ADJD')
                """
                pos_tag = tokens_tags[index][i]
                if pos_tag[1] == "ADJD" or pos_tag[1] == "ADJA":
                    compounds.append((index, i, token))


    splitter = Splitter()
    """
        Form:
        [(0.1740327189765392, 'Zucker', 'Süß'), (-1.5975678869950305, 'Zuck', 'Ersüß'), (-2.1849865951742626, 'Zuc', 'Kersüß'), 
        (-3, 'Zucke', 'Rsüß')]  
    """

    splitted_compounds = list()

    for compound in compounds:
    #     # form of compound:
    #     # (7, 2, ['19-3', '1557-1566', 'saukalt', 'Intensifier', '\n'])
        
        # form of splitted_compound = 
        # [(-0.5835459759340652, 'Wirk', 'Lich'), (-1.2466482494150914, 'Wir', 'Klich'), (-1.5259082915111741, 'Wirkl', 'Ich')] 
        # [(0.8513328138442754, 'Ein', 'Fach'), (-0.7000849466864454, 'Einf', 'Ach')]
        splitted_compound = splitter.split_compound(compound[2][2])

        if splitted_compound[0][0] > 0:
            lexem1 = str(splitted_compound[0][1]).lower()
            lexem2 = str(splitted_compound[0][2]).lower()
            splitted_compounds.append((compound[0], compound[1], compound[2][2], [lexem1, lexem2]))


    return splitted_compounds

def tag_compounds(splitted_compounds):
    
    # einzelne token des compounds
    #  ergänzen und dann
    # als compound elemente einfügen 
    # data in which compounds are splitted

    # [(7, 2, 'saukalt', ['Sau', 'Kalt'])]

    # create their pos-tag and annotation
    sent_tok_tag = dict()

    list_of_fail_annotated = list()

    for compound in splitted_compounds:
        # compound form:
        """
            (7, 2, 'saukalt', ['Sau', 'Kalt'])
        """

        tokens_tags = list()
        tagged_lexems = asptagger.tag_sentence(compound[-1])
        tokens_tags.append(tagged_lexems)

        # elements in token_tags are like
        """
            [('Sau', 'NN'), ('Kalt', 'ADJD')]
        """
    

        # Das will ich haben:
        # sau,    NN,     B-ITSF
        # kalt,   ADJD,   O
        #    später müsste hier ergänzt werden, ob es sem. steigerbar ist lol


        # will die form: 
        # sentence_id, token_id, [lex1, tag, BIO], [lex2, tag, BIO]

        if tokens_tags[0][1][1] == "ADJD":
            sent_tok_tag[compound[2]] = (tokens_tags[0][0][0], tokens_tags[0][0][1], "B-ITSF"), (tokens_tags[0][1][0], tokens_tags[0][1][1], "O")

        elif tokens_tags[0][1][1] == "ADJA":
            sent_tok_tag[compound[2]] = (tokens_tags[0][0][0], tokens_tags[0][0][1], "B-ITSF"), (tokens_tags[0][1][0], tokens_tags[0][1][1], "O")

        else:
            list_of_fail_annotated.append(compound)


    # dict entry looks like this:
    """
        {'saukalt': (('sau', 'ITJ', 'B-ITSF'), ('kalt', 'ADJD', 'O'))}
    """


    return sent_tok_tag

def labeling(sentences, tokens_tags):

    """
        BIO-Tagging:
        B-ITSF  --> Beginning of Intensifier
        I-InTSF --> Inside of Intensifier
        O       --> Outside of Intensifier
        Example:
            Ich	O
            hab	O	
            dann	O	
            auch	O	
            schnell	O	
            gewählt	O	
            und	O	
            saß	O	
            mit	O	
            meiner	O	
            sehr	B-ITSF	
            aufgeräumten	O	
            ,	O	
            gut	O	
            gelaunten	O	
            und	O	
            gesprächigen	O	
            Tochter	O	
            beim	O	
            Essen	O	
            .	O	
    """

    """
    2 Probleme. 
        gelöst         1.: Nicht alle I-ITSF werden mit * markeirt ???
        gelöst         2.: PoS wird benötigt.
    """
    label = list()

    for i, sentence in enumerate(sentences):
        sent_labels = list()

        # list, in which the tag sequence will be stored
        itsf_seq = list()

        for index, token in enumerate(sentence):
            # token in form of:
            """
                # ['18-3', '1557-1566', 'richtigen', '_', '\n']
                # ['18-2', '1551-1556', 'einem', '_', '\n']
            """
            # if token is not "_", it is marked as an intensifier
            if token[-2] != "_":
                
                # if "[" is not in the label of the token,
                # it is not part of a sequence of an intensifier
                if "[" not in token[-2]:
                    # and if the next token is also an adjd or adja
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

            # if token[-2] != "_":
            #     sent_labels.append("B-INTSF")
            # else:
            #     sent_labels.append("O")
        
        label.append(sent_labels)
    
    return label  

def annotation(tokens_tags, labels):
    documents = list()

    for index, sentence in enumerate(tokens_tags):
        sent_docs = list()
        for i, token_tag in enumerate(sentence):
            token = token_tag[0]
            pos_tag = token_tag[1]
            label = labels[index][i]

            sent_docs.append((token, pos_tag, label))
        
        documents.append(sent_docs)

    return documents

def test_and_train(documents):
    documents_amount = len(documents)
    train_amount = documents_amount / 100 * 80

    x_train = list()
    y_train = list()

    x_test = list()
    y_test = list()

    for amount, document in enumerate(documents):
        x_sent_info = list()
        y_sent_info = list()

        # if we're under the amount of the trainset
        if amount+1 < train_amount:
            for token in document:
                #print(token)
                x_sent_info.append((token[0], token[1]))
                y_sent_info.append(token[2])
        
            x_train.append(x_sent_info)
            y_train.append(y_sent_info)
            
        else:
            for token in document:
                x_sent_info.append((token[0], token[1]))
                y_sent_info.append(token[2])

            x_test.append(x_sent_info)
            y_test.append(y_sent_info)
        

    return x_train, y_train, x_test, y_test

def train_test():
    file_data = readfile()
    #file_data = readfile("8997_blog.xml.tsv")
    #print(file_data)

    sentences = get_sentences(file_data)
    #print(sentences)

    tokens_tags = pos_tagging(sentences)
    #print(tokens_tags)

    splitted_compounds = split_compounds(sentences, tokens_tags)
    #print(splitted_compounds)

    tagged_compounds = tag_compounds(splitted_compounds)
    #print(tagged_compounds)
    keys = tagged_compounds.keys() 
    #print(keys)

    #labeling(sentences, tokens_tags)
    labels = labeling(sentences, tokens_tags)
    #print(labels)

    work_annot = annotation(tokens_tags, labels)

    # documents which beholds each annotation for each token in a sentence
    # devided by sentences
    documents = list()

    #adding the splitted compounds to the data
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
        
        documents.append(document)

    training_data, test_data = train_test_split(documents, test_size=0.2, shuffle=False)
    
    return training_data, test_data 
    

if __name__ == "__main__":

    training_data, test_data = train_test()


    print(len(training_data))
    print(len(test_data))
