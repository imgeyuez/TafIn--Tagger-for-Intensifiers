"""
    The first baseline will be the grouptag for intensifier,
    focus- and gradparticel from the someweta module itself. 

    Therefore the baseline is nothing but the def pos_tagging(sentences)
    where the tokens tagged with ... will be marked as intensifiers.
"""

def baseline_first(tagged_tokens):
    y_pred = list()
    for token_tag in enumerate(tagged_tokens):
        #print(token_tag[1][1])
        if token_tag[1][1] == "PTKIFG":
            y_pred.append(1)
        else:
            y_pred.append(0)

    return y_pred
