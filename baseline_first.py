"""
    The first baseline will be the grouptag for intensifier,
    focus- and gradparticel from the someweta module itself. 

    Therefore the baseline is nothing but the results of
    def pos_tagging(sentences) where the tokens tagged 
    with PTKIFG will be marked as intensifiers.
"""

def baseline_first(x_test):
    y_pred = list()

    for doc in x_test:
        sent_pred = list()

        for index, token in enumerate(doc):
            # if token is marked as an intensifier
            if token[1] == "PTKIFG":
                # check, if token before is also one
                # if not, it is the beginning of an intensifier
                # if yes, it is the continuation of an intensifier
                if doc[index-1] !="PTKIFG":
                    sent_pred.append("B-ITSF")
                else:
                    sent_pred.append("I-ITSF")
            else:
                sent_pred.append("O")

        y_pred.append(sent_pred)

    return y_pred
