"""
Das folgende Programm präsentiert die erste Baseline.
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


def itsf_identification(sentences):
    pass

def run_script(filenames):
    pass


if __name__ == "__main__":

    filename = "test_on_data5.tsv"

    #run_script(filenames)