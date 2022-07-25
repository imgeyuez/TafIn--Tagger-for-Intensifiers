"""
    The first baseline will be the grouptag for intensifier,
    focus- and gradparticel from the someweta module itself. 

    Therefore the baseline is nothing but the def pos_tagging(sentences)
    where the tokens tagged with PTKIFG will be marked as intensifiers.
"""

def baseline_first(test_data):
    # list for lable predictions
    y_pred = list()
    # go through each token in the data
    for token in test_data:
        # if it has the tag, append 1 for the lable "intensifier"
        if token[1] == "PTKIFG":
            y_pred.append(1)
        # else append 0 for "not intensifier"
        else:
            y_pred.append(0)

    return y_pred
