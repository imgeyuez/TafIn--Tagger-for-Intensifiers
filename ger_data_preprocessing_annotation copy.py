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
        token = content[2]
        sentence.append(token)
        
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
    #print("\n".join(["\t".join(t) for t in tagged_sentence]), "\n", sep="")
 
# print(len(used_content))
#print(tagged_tokens)

##########  tokens und intensivierer in neue        ##########
##########  datei zum annotieren übertragen         ########## 

with open("test_newdatafile.txt", "w", encoding="UTF-8-sig") as newfile:
    for index, token in enumerate(tagged_tokens):
        # look if token is in front of an Adjective
        if tagged_tokens[index+1][1] == "ADJD" or tagged_tokens[index+1][1] == "ADJA":
            ifoA = 1
        else:
            ifoA = 0

        # look if token is ADJD or ADJA
        if tagged_tokens[index][1] == "ADJD":
            DoA = "pred"
        elif tagged_tokens[index][1] == "ADJA":
            DoA = "att"
        else:
            DoA = "None"
        
        # look, if token is an intensifier
        


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