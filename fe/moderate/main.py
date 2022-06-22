from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle
import spacy
import string
import praw
import re
import time
import csv
from WebScraping import scrapeReddit


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

def MODeRATE(MOD, n):
    return RFR_AI_model(scrape_n_posts(MOD, n))

def RFR_AI_model(comments):
    cleaned = []
    nlp = spacy.load("en_core_web_sm")
    for message in comments:
        str = ""
        doc = nlp(message)
        for token in doc:
            if not token.is_stop and not (token.text in string.punctuation) and token.text!= "\n":
                str += token.lemma_.lower() + " "
        cleaned.append(str[0:len(str)-1])
    
    model = pickle.load(open("C:/Users/Yan Rong/Documents/programming/Orbital/RFR_model.sav", 'rb'))
    ratings = model.predict(cleaned)
    average = sum(ratings)/len(ratings)
    return (comments, f'{average:.2f}')

def NB_AI_model(comments):
    model = pickle.load(open("NB_model.sav", 'rb'))
    ratings = model.predict(comments)
    average = sum(ratings)/len(ratings)
    return (comments, average)
