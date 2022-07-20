import spacy
import string
import pandas as pd
#RFR MODEL
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle

dataset = pd.read_csv("Comments Review - Sheet1.csv")[["Comment","Emotion","Rating"]]

def text_preprocess(comments):
    cleaned = []
    nlp = spacy.load("en_core_web_sm")
    for message in comments:
        str = ""
        doc = nlp(message)
        for token in doc:
            if not token.is_stop and not (token.text in string.punctuation) and token.text!= "\n":
                str += token.lemma_.lower() + " "
        cleaned.append(str[0:len(str)-1])
    return cleaned

RFR = Pipeline([
    ('count vectorizer', CountVectorizer()),
    ('chi2score', SelectKBest(chi2,k=50)),
    ('tf_transformer', TfidfTransformer()),
    ('regressor', RandomForestRegressor())
])

model1 = RFR.fit(text_preprocess(dataset["Comment"]), dataset["Rating"])

pickle.dump(model1, open("RFR_model.sav", 'wb'))