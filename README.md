# TafIn--Tagger-for-Intensifiers
An implementation, which can be used for an automatic identification of intensifiers of adjectives in German. This model is trained on a german corpus, therefore the automatic identification will only be available for the German language so far.

As this is the project of my bachelor thesis, there are also baselines within this repository, which were needed for a comparation in the evaluation.  

The thesis itself might be uploaded after the grading.

The model was trained and tested on Python 3.10.2.


## 1. Requirements to run the model:
In order for the model to run smoothly there is the need to install the following modules/packages:     
* numpy           1.23.1   `pip install numpy`
* python-crfsuite 0.9.8    `pip install python-crfsuite`
* SoMeWeTa        1.8.0    `pip install SoMeWeTa`
* charsplit       0.1      To use charsplit, please go to https://github.com/dtuggener/CharSplit, download the folder "charsplit" and unpack it in the same folder as the implementation files for this project are safed in.


## 2. Usage
As this project is specificly designed to fit a certain data arrangement, the main.py file is only useful if one has access to the data (see paper).
As the data is important for the preprocessing, it is not possible yet to continue the usage of TafIn with the main.py file. 
The arrangement for the data is like: 
```
# Sentence
Sentencenumber-tokennumber \t Startindex-Endindex \t Token \t Annotation "_" or "Intensifier"
Example:
#Text=This is an example.
1-1   0-4   This  _
1-2   5-7   is _
1-3   8-10  an _
1-4   11-18 example  _
1-5   18-19 .  _
```

**Please note, that while using the program, it can take a while until something is shown on the terminal as it needs some time to import and process some of the various (preprocessing) steps.**

### 2.1 With access to the data
With access to the specific data (or data that is structured in the same way), one only needs to save the datafiles (-tsv-files) and all the implementation files within the same folder. 
If the requirements are also fullfilled, main.py can be run and the user is guided through the application of TafIn.
Therefore no adjustments are needed.

1. Starting the program.

   The program starts when all the requirements are fullfilled and main.py is executed.
2. After the data is preprocessed, a menu will pop up with the following options:

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
           
           `1 Train model again.`: Trains the model again (or a new model) to use it on the testdata afterwards. 
           
           `2 Use trained model on test data.`: Skips the step to train the model and uses the pretrained model file `crf.model` on the test data.
        * `Should the output be printed?`
           
           `0 No`: No Output will be printed.
           
           `1 Yes`: Output will be printed.
        * `Should the results of the evaluation be printed?` 
           
           `0 No`: No evaluation will be printed.
           
           `1 Yes`: Results of the evaluation will be printed. 

### 2.2 No access to the data
The trained model is accessable but the data needs to bee in the same arrangement, to use main.py .

To get access to the used data please look here: [TwiBloCoP by Scheffler et al. (2022)](http://staff.germanistik.rub.de/digitale-forensische-linguistik/forschung/textkorpus-sprachliche-variation-in-sozialen-medien/)

If you have your own data, please orientate yourself on the required arrangements to generate features for each token here: [
scrapinghub / python-crfsuite](https://github.com/scrapinghub/python-crfsuite)

Once the data is aquired, follow the steps in 2.3.

### 2.3 Use only pretrained model without main.py
To use the pretrained TafIn model, type:

```
import pycrfsuite

tagger = pycrfsuite.Tagger()
tagger.open("crf.model")
y_pred = [tagger.tag(xseq) for xseq in x_test]
```

Where x_test contains the inputs (token, postag) for every token in every sentence xseq like:

```
x_test = [[("Das", "PDS"), ("ist", "VAFIN"), ("ein", "ART"), ("Beispiel", "NN"), (".", "$.")], 
    [(Es, "PPER"), ("sollte", "VMFIN"), (so, "ADV"), ("aussehen", "VVINF"), (".", "$.")]]
```
