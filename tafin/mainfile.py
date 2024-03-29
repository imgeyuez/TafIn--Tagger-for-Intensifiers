"""
    This file is the main file of the project.
    It is designed to lead through all the steps which were involved to get to the 
    result of the thesis.
    Therefore it might be uninteresting and irrelevant for outsinders. 
    
    It only runs if the data, which is used for training and testing, is
    within the same folder as all the files in the tafin-folder in this
    github repository.
    
    If run, the data will be preprocessed. 
    After that a menu pops up that guides the user through various 
    steps.
    For more details please refer to the README document.
"""
#####################################
#   modules
#####################################
from preprocessing import train_test
from evaluate import evaluation

#####################################
#   functions
#####################################

def get_inputs(doc):
    """
        Function to extract the tokens and pos-tags 
        as input for the model from the test data.
        Input:
        1. doc (list)               :   List, that contains token and pos-tag 
                                        input from the test data.
        1. (token, postag) (tuple)  :   Tuple containing the token and the 
                                        pos-tag.
    """
    return [(token, postag) for (token, postag, label) in doc]
    
def get_labels(doc):
    """
        Function to extract the labels as goldlabels 
        for the model from the test data.
        Input:
        1. doc (list)   :   List, that contains token and pos-tag 
                            input from the test data.
        1. label (str)  :   String containing the label.
    """
    return [label for (token, postag, label) in doc]

def run_script():
    """
        First, the data, used for the models will be generated.
        Afterwards a menu pops up, where the user gets guided
        through the implementations and their evaluation - if wanted.
        Input:
            None.
        Output:
            None. 
            There will either be printed outputs in the terminal
            (or maybe generated datafiles). 
    """

    print("\STARTED:\tPreprocessing the data.\n")

    # generate the train and test data
    training_data, test_data = train_test()

    print("\nFINISHED:\tPreprocessing the data.\n")

    print("\SARTED:\tGenerating test data.\n")

    # generating the inputs for the testdata
    x_test = [get_inputs(doc) for doc in test_data]

    # extract the labels from the testdata
    y_test = [get_labels(doc) for doc in test_data]

    print("\nFINISHED:\tGenerating test data.\n")

    while True:
        print("""
        This is the user guide to present the project. 
        As there were many steps involved to establish this program,
        there will at least be the option, to run through them 
        all seperatly, to get impressions of how they work. 

        To chose options in the following process
        type in the number in front of the option and hit enter.""")

        # ask user which model should be used
        model = int(input("Which model do you want to use/evaluate?\nPlease choose one of the following:\n0\tClose program.\n1\tBaseline 1\n2\tBaseline 2\n3\tTafIn\n\n"))
        try: 
            if model == 0:
                break 

            elif model == 1:
                print_output = int(input("Should the output be printed?\n0\tNo\n1\tYes\n"))
                print_evaluation = int(input("Should the results of the evaluation be printed?\n0\tNo\n1\tYes\n"))

                # import first baseline
                from baseline_first import baseline_first

                print("STARTED:\tLabelprediction with Baseline 1.")

                # label predictions from baseline 1:
                y_pred_b1 = baseline_first(x_test)

                print("FINISHED:\tLabelprediction with Baseline 1.")

                if print_output == 1:
                    print("STARTED:\tPrinting labelprediction of Baseline 1.")

                    print(y_pred_b1)

                    print("FINISHED:\tPrinting labelprediction of Baseline 1.")

                elif print_output == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")

                if print_evaluation == 1:
                    print("STARTED:\tEvaluation of Baseline 1.")

                    print(evaluation(y_test, y_pred_b1))

                    print("FINISHED:\tEvaluation of Baseline 1.")

                elif print_evaluation == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")

            elif model == 2:
                print_output = int(input("Should the output be printed?\n0\tNo\n1\tYes\n"))
                print_evaluation = int(input("Should the results of the evaluation be printed?\n0\tNo\n1\tYes\n"))

                # import first baseline
                from baseline_second import baseline_second

                print("STARTED:\tLabelprediction with Baseline 2.")

                # label predictions from baseline 1:
                y_pred_b2 = baseline_second(x_test)

                print("FINISHED:\tLabelprediction with Baseline 2.")

                if print_output == 1:
                    print("STARTED:\tPrinting labelprediction of Baseline 2.")

                    print(y_pred_b2)

                    print("FINISHED:\tPrinting labelprediction of Baseline 2.")

                elif print_output == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")


                if print_evaluation == 1:
                    print("STARTED:\tEvaluation of Baseline 2.")

                    print(evaluation(y_test, y_pred_b2))

                    print("FINISHED:\tEvaluation of Baseline 2.")
                
                elif print_evaluation == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")

            elif model == 3:
                from tafin import train_tafin, test_tafin
                train_model = int(input("A trained model is available. Should the process of training be repeated or just the trained model used on the test data?\n1\tTrain model again.\n2\tUse trained model on test data.\n\n"))
                print_output = int(input("Should the output be printed?\n0\tNo\n1\tYes\n\n"))
                print_evaluation = int(input("Should the results of the evaluation be printed?\n0\tNo\n1\tYes\n\n"))

                if train_model == 1:
                    # train tafin
                    print("STARTED:\tTraining TafIn.")
                    
                    train_tafin(training_data)

                    print("FINISHED:\tTraining TafIn.")

                elif train_model == 2:
                    # predicit with tafin 
                    print("STARTED:\tLabelprediction with TafIn.")
                    
                    y_pred_tafin = test_tafin(test_data)

                    print("FINISHED:\tLabelprediction with TafIn.")
                
                else:
                    print("Invalid input. Please try again.")

                if print_output == 1:
                    print("STARTED:\tPrinting labelprediction of TafIn.")

                    print(y_pred_tafin)

                    print("FINISHED:\tPrinting labelprediction of TafIn.")

                elif print_output == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")

                if print_evaluation == 1:
                    print("STARTED:\tEvaluation of TafIn.")

                    print(evaluation(y_test, y_pred_tafin))

                    print("FINISHED:\tEvaluation of TafIn.")
                
                elif print_evaluation == 0:
                    pass

                else:
                    print("Invalid input. Please try again.")   

        except:
            print("Your input is invalid. Please try again.")


#####################################
#   main
#####################################

# execution of all steps
if __name__ == "__main__":
    
    run_script()
