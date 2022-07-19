# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
import pandas as pd
import pickle
import spacy
import string
import praw
import sys
sys.path.insert(1, 'C:/Orbital/Orbital_Moderate')
from WebScraping import scrapeReddit
from collections import Counter
import text2emotion as te

CLIENT_ID = "HJFREmWRT9QTnbohyZup6w"
CLIENT_SECRET = "S__YD99jhRGHnwWjzMFZTDlQeT18RA"
USER_AGENT = "Orbital"

# Reddit Instance
reddit_read = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# Subreddits
nus_sub = reddit_read.subreddit("nus")
def scrape_n_posts(mod, n):
    return scrapeReddit.scrape_posts(mod, nus_sub, n) 

#NLTK VADER
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def SIA_analyse_sent(comments):
    sia = SIA()
    results = []
    for comment in comments:
        pol_score = sia.polarity_scores(comment)
        pol_score["Comment"] = comment
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)
    return (comments, df["compound"].mean())

#def MODeRATE(MOD, n):
#    return RFR_AI_model(scrape_n_posts(MOD, n))

def RFR_AI_model_predict(comments): #input list of strings
    #PATH = "C:/Orbital/Orbital_Moderate/fe/moderate/RFR_model.sav"
    PATH = 'https://github.com/ZhiQi12/Orbital-/blob/master/fe/moderate/RFR_model.sav'
    model = pickle.load(open(PATH, 'rb'))
    ratings = model.predict(comments)
    return ratings

def text_preprocessing(comments):
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

def RFR_avg_rating(comments):
    cleaned = text_preprocessing(comments)
    ratings = RFR_AI_model_predict(cleaned)
    average = sum(ratings)/len(ratings)
    return f'{average:.2f}'

def merge_dict(dict1, dict2):
    final_dict = {}
    for key in dict1.keys():
        if key in dict2.keys():
            final_value = dict1[key] + dict2[key]
        else:
            final_value = dict1[key]
        final_dict[key] = final_value
    for key in dict2.keys():
        if key not in final_dict.keys():
            final_dict[key] = dict2[key]
    return final_dict

def get_emotion_dict(comment):
    return te.get_emotion(comment)

def emotion_chart(comments):
    emotions_dict = {"Happy": 0.0, "Angry" : 0.0, "Surprise" : 0.0, "Sad" : 0.0, "Fear" : 0.0}
    for comment in comments:
        emotions_dict = merge_dict(emotions_dict, get_emotion_dict(comment))
    return list(emotions_dict.values())

def convert_emotion_chart_to_str(emotions):
    emo_string = ""
    for e in list(map(str, emotions)):
            emo_string += e + ","
    return emo_string[:-1]