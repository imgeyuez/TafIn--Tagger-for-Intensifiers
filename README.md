# TafIn--Tagger-for-Intensifiers
An implementation with the goal of a model, which can be used for an automatic identification of intensifiers of adjectives in German. This modell is trained on an german corpus, therefore the automatic identification will only be available for the German language so far.

As this is the project of a thesis, there are also baselines within this repository, which were needed for a comparation in the evaluation.  


## Requirements to run the model:
In order for the model to run smoothly there is the need to install the following modules/packets:
* charsplit       0.1     
* numpy           1.23.1  
* python-crfsuite 0.9.8    
* SoMeWeTa        1.8.0   

```
pip install
pip install
pip install
```

## Usage
As this project is specificly designed to fit a certain data arrangement, the main.py file is only useful if one has access to the data (see paper).
As the data is important for the preprocessing, it is not possible yet to continue the usage of TafIn without it. 

**Please note, that while using the program, it can take a while until something is shown on the terminal as it takes a while to impoert and work through some of the various steps.**

### With access to the data
With access to the specific data (or data that is structured in the same way), one only needs to save the data (-tsv-files) and all the implementation files within a same folder. 
If the requirements are also fullfilled, main.py can be run and the user is guided through the application of TafIn.
Therefore no adjustments are needed.

1. Starting the program.

   The program starts when all the requirements are fullfilled and main.py is executed.
2. After the data is preprocessed, a menue will pop up with the following options:

   ```
   0  Close program
   1  Baseline 1
   2  Baseline 2
   3  TafIn
   ```
   
3. Based on the choosen option, one of the following next steps will occur:

    1. Option `0 Close program`:
        
        Closes the program.
    2. Option `1 Baseline 1`:
    
        Leads to the labelprediction of baseline 1 and to the option to see the evaluation of it. The user can choose between:
        
        * `Should the output be printed?` 
        
           `0 No`: No Output will be printed.
           
           `1 Yes`: Output will be printed.
        * `Should the results of the evaluation be printed?` 
           
           `0 No`: No evaluation will be printed.
           
           `1 Yes`: Results of the evaluation will be printed. 

    3. Option `2 Baseline 2`:
    
        Leads to the same options as option 1 but this time with results from the second baseline.
        
    4. Option `3 TafIn`:
        
        Leads to the mainfocus of this project. Here are three options available. 
        
        * `A trained model is available. Should the process of training be repeated or just the trained model used on the test data?`
           
           `1 Train model again.`: Trains the model again to use it on the testdata afterwards. 
           
           `2 Use trained model on test data.`: Skips the step to train the model and uses the pretrained model file `tafin_crf.model` on the test data.
        * `Should the output be printed?`
           
           `0 No`: No Output will be printed.
           
           `1 Yes`: Output will be printed.
        * `Should the results of the evaluation be printed?` 
           
           `0 No`: No evaluation will be printed.
           
           `1 Yes`: Results of the evaluation will be printed. 


### No access to the data - Not provided yet.
The trained model is accessable but there is no provided guide on how to use it yet.
