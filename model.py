import spacy
import textract
import re
from config import spacy_700_path,tagvalues_spacy

def ocr(filename):
    #ocr
    text = str(textract.process(filename))
    
    #little pre-processing
    text = re.sub('\n'," ",text)
    text = re.sub(r'[^\x00-\x7f]',r'', text)
    return text 

def spacy_700(text):
    o1 = {}
    spacy_700_list = []
    model_spacy_path_all = spacy_700_path

    model_spacy = spacy.load(model_spacy_path_all)

    # predict
    doc = model_spacy(text)
    for ent in doc.ents:
        if ent.label_.upper() in tagvalues_spacy:
            temp = {f'{ent.label_.upper():{4}}': [ent.text]}
            spacy_700_list = spacy_700_list + [temp]
    for val in spacy_700_list:
        o1.update(val)
        
    #del model_spacy
    return o1

 
