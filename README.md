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
As this project is specificly designed to fit a certain data arrangement, the ui.py file is only useful if one has acces to the data (see paper). 

### With access to the data
With access to the specific data, one only needs to save the data and all the implementation files within a same folder. 
If the requirements are also fullfilled, main.py can be run and the user is guided through the application of TafIn.
Therefore no adjustments are needed.

### No access to the data - Not provided yet.
The trained model is accessable but there is no provided guide on how to use it yet.
