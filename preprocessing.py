"""
    This file is for the preprocessing of the data.
    Good thing is that the data is already tokenized.
    That will be helpful.
    Results are supposed to be:
    > PoS-Tagged Tokens
    > Splitting adjectivecompounds that were annotated as intensifiers

    So to be able to use this preprocessing file unproblematicly,
    the data has to be already tokenized.
"""

### To Do ###
# split adjective compounds that are marked as intensifiers
# add comments 


from someweta import ASPTagger


def readfile(filename):
    """
        Reads the file and saves its content within a variable.
        One row of the data is one entry within the list file_input
    """
    with open(filename, encoding="UTF-8-sig") as file:
        file_input = file.readlines()

    return file_input

def get_sentences(file_input):
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

    # go through the input from the file
    for i in range(len(file_input)):

        # ...split the input...
        content = file_input[i].split("\t")
        # extract the token
        token = content[0]
        # append the token to generate the one sentence
        sentence.append(token)

        if token == ".":
            sentences.append(sentence)
            sentence = []

    return sentences

    
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


def run_script(filename):
    file_input = readfile(filename)
    sentences = get_sentences(file_input)
    tagged_tokens = pos_tagging(sentences)
    print(tagged_tokens)

if __name__ == "__main__":

    filename = "test_on_data5.txt"

    run_script(filename)
