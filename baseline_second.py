"""
Das folgende Programm präsentiert die zweite Baseline.
Baselines werden verwendet, um vergleichen zu können, ob sich das 
implementierte Programm "lohnt" oder keinen Unterschied zu vorherigen
Methoden macht.

Die 1. Baseline: 
    POS-Tags ADJD & ADJA herausfiltern und das links davon
    stehende Element als Intensivierer markieren, solange es kein 
    Verb ist
    Also sprich: einfach eine heuristische Methode

Die 2. Baseline:
    Kann ein Modell von dem Empirist Modell darstellen mit ihrer 
    Sammelklasse von Fokus- Graduierungs- und Intensitätspartikeln. 
    Das von someweta

Könnte auch ne 3. Baseline einbauen, bei der mit den Wörterlisten
nach weiteren Intensivierern geschaut wird, aber weiß nicht, inwieweit
das schon zu viel wäre .. hmm
"""

# if-Bedingung, ob es sich bei Token um ein Adjektiv handelt
    # if token == ADJD or token == ADJA:
        # gucken, was das Objekt links daneben ist:
            # if token[-1] nicht Verb, nicht Determinant: markiere
                # es als Intensivierer
            #else: pass
    # else: pass

def baseline_two(data):
    """
        Identification of intensifiers with heuristic method:
        Token in front of an adjective, that is not a verb

        Won't find intensifiers as in
        Super cool.
        Das ist ein bisschen blöd.
        Ganz ganz super gemacht.
        
    """
    # import re
    # pattern = r"VAFIN [A-Z]+ (ADJD|ADJA)"

def baseline_two(data):
    import re
    pattern = r"VAFIN [A-Z]+ (ADJD|ADJA)"

    y_pred = list()
    tags = list()
    for token in data:
        tags.append(token[1])

    tags_len = len(tags)
    for index, tag in enumerate(tags):
        if index != tags_len-1:
            try:
                if tags[index+1] == "ADJA" or tags[index+1] == "ADJD":
                    if tags[index-1] == "VAFIN":
                        print(tags[index-1], tag, tags[index+1])
                        y_pred.append(1)

                    else:
                        y_pred.append(0)
                else:
                    y_pred.append(0)
            except:
                y_pred.append(0)

    return y_pred