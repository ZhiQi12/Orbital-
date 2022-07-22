# main.py
import pandas as pd
import pickle
import spacy
import string
import praw
import sys
#sys.path.insert(1, 'C:/Users/Yan Rong/Documents/GitHub/Orbital-')
from WebScraping import scrapeReddit
import text2emotion as te

CLIENT_ID = "HJFREmWRT9QTnbohyZup6w"
CLIENT_SECRET = "S__YD99jhRGHnwWjzMFZTDlQeT18RA"
USER_AGENT = "Orbital"

# Reddit Instance
reddit_read = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# Subreddits
nus_sub = reddit_read.subreddit("nus")

# load csv and create empty df
mods = pd.read_csv("mods.csv")
df = pd.DataFrame(columns = ["id", "code","rating","comment1","comment2","comment3","searched","emotions"])

def scrape_n_posts(mod, n):
    return scrapeReddit.scrape_posts(mod, nus_sub, n) 

def RFR_AI_model_predict(comments): #input list of strings
    #PATH = "C:/Users/Yan Rong/Documents/GitHub/Orbital-/fe/moderate/RFR_model.sav"
    PATH = "RFR_model.sav"
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

    ec = list(emotions_dict.values())
    final = []
    for e in ec:
        final.append(e/sum(ec)*100)
    return final

def convert_emotion_chart_to_str(emotions):
    emo_string = ""
    for e in list(map(str, emotions)):
            emo_string += e + ","
    return emo_string[:-1]


# main function to load the entire csv file
def update(df, mods):
    counter = 1
    for mod in mods["Module Code"]:
        
        tpl = scrape_n_posts(mod, 3)
        if tpl != ([], []):
            try:
                comment1 = tpl[1][0]
            except:
                comment1 = ""
            try:
                comment2 = tpl[1][1]
            except:
                comment2 = ""
            try:
                comment3 = tpl[1][2]
            except:
                comment3 = ""

            df = df.append({'id':counter,'code':mod, 'rating':RFR_avg_rating(tpl[0]), 'comment1':comment1,
                    'comment2':comment2, 'comment3':comment3, 'searched':0,
                    'emotions':convert_emotion_chart_to_str(emotion_chart(tpl[0]))}, ignore_index=True)
            counter +=1
        else:
            pass
    return df
    
# functin which finds the information for 1 mod
def singleMod(mod):
    tpl = scrape_n_posts(mod, 3)
    if tpl != ([], []):
        try:
            comment1 = tpl[1][0]
        except:
            comment1 = ""
        try:
            comment2 = tpl[1][1]
        except:
            comment2 = ""
        try:
            comment3 = tpl[1][2]
        except:
            comment3 = ""
        
    rating = RFR_avg_rating(tpl[0])
    searched = 0
    emotions = convert_emotion_chart_to_str(emotion_chart(tpl[0]))
    return (mod, rating, comment1, comment2, comment3, searched, emotions)

# save df into csv file

if __name__=='__main__':
    # updated_df = update(df, mods)
    # updated_df.to_csv("moderate_mods.csv", index=False)
    x = singleMod('is1103')
    with open("test.txt", 'w') as f:
        f.write(x[2])

