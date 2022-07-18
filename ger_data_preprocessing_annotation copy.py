"""
Innerhalb dieser Datei werden die einzulesenen Daten vorbereitet.
D.h.:
> Tokenisieren
> POS ergänzen 
> Aufsplitten von ADJD/ADJA als Komposita 
"""

import re
from someweta import ASPTagger

def readfile(file):
    pass

##########  read in the data    ##########
with open("test.tsv",encoding="UTF-8-sig") as file:
    file_input = file.readlines()

used_content = []
sentence = []
sentences = []

for i in range(len(file_input)):
    pattern = re.search(r"[0-9]+-[0-9]+", file_input[i])
    if pattern:
        content = file_input[i].split("\t")
        used_content.append(content)
        token_tag = content[2]
        sentence.append(token_tag)
        
    else:
        if sentence != []:
            sentences.append(sentence)

        sentence = []


# das ist eigentlich effizienter, aber der letzte Satz
# geht mir hier verloren
"""
    for line in file_input:
        pattern = re.search(r"[0-9]+-[0-9]+", line)
        if pattern:
            line_content= line.split("\t")
            token = line_content[2]
            sentence.append(token)
        else:
            if sentence != []:
                sentences.append(sentence)

            sentence = []
"""

##########  PoS-tagging ##########

# pretrained model form someweta
model = "german_web_social_media_2020-05-28.model"

asptagger = ASPTagger()
asptagger.load(model)

tagged_tokens = list()
for sentence in sentences:
    tagged_sentence = asptagger.tag_sentence(sentence)
    for index in range(len(tagged_sentence)):
        tagged_tokens.append(tagged_sentence[index])

# print(len(used_content))


##########  tokens und intensivierer in neue        ##########
##########  datei zum annotieren übertragen         ########## 

with open("test_newdatafile.txt", "w", encoding="UTF-8-sig") as newfile:
    for index, token_tag in enumerate(tagged_tokens):
        # look if token is in front of an Adjective
        try:
            if tagged_tokens[index+1][1] == "ADJD" or tagged_tokens[index+1][1] == "ADJA":
                ifoA = 1
            else:
                ifoA = 0
        except:
            pass

        # look if token is ADJD or ADJA
        if token_tag[1] == "ADJD":
            DoA = "pred"
        elif token_tag[1] == "ADJA":
            DoA = "att"
        else:
            DoA = "None"
        
        # look, if token is an intensifier
        if used_content[index][3] == "_":
            itsf = 0
        else:
            itsf = 1
        
        # apply to new file
        information = str(token_tag[0]) + "\t" + str(ifoA) + "\t" + str(DoA) + "\t" + str(itsf) + "\n"
        newfile.write(information)


# with open("test_newdatafile.txt", "w", encoding="UTF-8-sig") as newfile:
#     for used, tagged in zip(used_content, tagged_tokens):
#         add = str(used[2]) + "\t" + str(tagged[1]) + "\n"
#         newfile.write(add)

"""
with open("newdatafile.txt", "w", encoding="UTF-8-sig") as newfile:
    for i in range(len(file_input)):
        if file_input[i][3] == "_":
            add = str(file_input[i][2]) + "\t0\n"
            newfile.write(add)
        else:
            add = str(file_input[i][2]) + "\t1\n"
            newfile.write(add)
"""

print("Fertig")
