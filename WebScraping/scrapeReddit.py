from ast import Store
import datetime
from tabnanny import check
from unittest.util import three_way_cmp
from numpy import true_divide
import praw
import pandas as pd
import re
from requests import post
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from scrapeNUSMODS import *
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from praw.models import MoreComments
import time

import csv


pd.set_option("display.max_columns", 100)

CLIENT_ID = "HJFREmWRT9QTnbohyZup6w"
CLIENT_SECRET = "S__YD99jhRGHnwWjzMFZTDlQeT18RA"
USER_AGENT = "Orbital"

# Reddit Instance
reddit_read = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# Subreddits
nus_sub = reddit_read.subreddit("nus")

#Print display_name, title, description (info of subreddit)
def get_subredditInfo(subreddit):
    print(subreddit.display_name)
    print(subreddit.title)
    print(subreddit.description)

# Scrape functions
def find_top_2(subreddit):
    for post in subreddit.hot(limit=2):
        print("Title = "+ post.title)
        print("Full Post = " + post.selftext)
        print("Number of Upvotes = " , post.score)
        print("Number of Comments = ", post.num_comments)
        print()

# Scrape function (using pandas) 
def scrapeTopPosts(subreddit):
    #posts = subreddit.top("month")
    posts_dict = {"Title": [], "Post Text": [], "Score": [],
              "Total Comments": [], "Post URL": [] }

    for post in subreddit.hot(limit=30):  
        posts_dict["Title"].append(post.title)
        posts_dict["Post Text"].append(post.selftext)
        posts_dict["Score"].append(post.score)
        posts_dict["Total Comments"].append(post.num_comments)
        posts_dict["Post URL"].append(post.url)

    top_posts = pd.DataFrame(posts_dict)
    return top_posts


keywords = ["mods", "modules"]
modList = ["CS", "BT", "GE", "IS"]  #May need the prefix of all mods?


# Scraping posts while filtering for mods , returns a dataFrame with posts info
def scrapeModPosts(subreddit, limitNum):
    #posts = subreddit.top("month")
    
    modPosts_dict = {"Title": [], "Post Text": [], "Score": [],
              "Total Comments": [], "Post URL": [], "Time Posted": [], "ID": []
              }

    for post in subreddit.hot(limit=limitNum):

            for word in post.title.split(" "):  #for each word in the post title(its type is list)
                # if post.id not in modPosts_dict["ID"]:

                #     if word in keywords or checkMods(modList, word):
                if filterPost(modPosts_dict, word, post.id, "ID"):

                    modPosts_dict["Title"].append(post.title)
                    modPosts_dict["Post Text"].append(post.selftext)
                    modPosts_dict["Score"].append(post.score)
                    modPosts_dict["Total Comments"].append(post.num_comments)
                    modPosts_dict["Post URL"].append(post.url)
                    modPosts_dict["Time Posted"].append(datetime.datetime.fromtimestamp(post.created))
                    modPosts_dict["ID"].append(post.id)

                    #print(getComments(post)) #comments 
        
    top_posts = pd.DataFrame(modPosts_dict)
    return top_posts

# Scraping posts while filtering for mods , returns a dataFrame with post objects
def scrapeModPosts2(subreddit, limitNum):
    dict = {"ID": [], "Title": [], "Post Object": []
    }
    for post in subreddit.hot(limit=limitNum):

        for word in post.title.split(" "):  #for each word in the post title(its type is list)
            if filterPost(dict, word, post.id, "ID"):
                dict["Title"].append(post.title)
                dict["ID"].append(post.id)
                dict["Post Object"].append(post) 
    
    df = pd.DataFrame(dict)
    return df

# Function to check module name/wildcard 

def checkMods(modList, word):
    for mod in modList:
        modString = mod + "...."
        temp = re.compile(modString) 
        if bool(temp.search(word)):
            return True
        else:
            continue
    return False

def addCommentsToCSV(comments):
    with open('./comments.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        for comment in comments:
            writer.writerow([comment])

def clearCSV():
    # Truncates the csv file
    f = open('./comments.csv', 'w+')
    f.close()

def getCommentList(comments):
    addCommentsToCSV(comments)
###################################################################################################################################################
banned_words = ["telegram", "textbook","textbooks", "tele", "chats","grp", "group","chat","modreg", "internship", "friends", "notes", "bid", "bidding"]
banned_words_for_comments = ["thank", "thanks", "?", "thx"]
    # look at post title and filter out (telegram, textbooks, grp chats, internship, pyp, friends etc)
    # post upvote most be >= 5 and time < 3 yrs
    # comment requirements : > words, >3 upvote / look at % of post's upvote and can assign to different bands, NEED TO DECIDE ON THIS
    # 0) merge post title and post self text to filter tgt
    # 1) check for banned_words
    # 2) time => if within 2 weeks, dun need check upvote. Elif >= 3 years, dun scrape. Elif > 2 wks + < 3yrs, need check upvote 
    # 3) check if title got module name
    # 4) Comments: question mark, "thank you", less than 7 
    # 5) Post selftext: "bid"
    # 

def check_date(post): 
    date_posted = post.created_utc  # date posted
    today = time.time()  # today's time
    two_weeks = 1209600
    three_yrs = 94608000
    diff = float(today) - float(date_posted)
    if diff >= three_yrs:
        return -1  # don't scrape
    elif diff < two_weeks:
        return 1   # scrape, don't need check upvote because very recent
    else:
        return 0   #check upvote then can scrape


def scrape_posts(mod, subreddit, n):
    dict = {"Post Title": [], "Comments":[]}
    counter = 1
    #banned_words = ["telegram", "textbooks", "tele", "chats"]
    for post in subreddit.search(mod):
        
        if counter <= n and filterPost(post, banned_words, mod):
            check_date_num = check_date(post)
            comments = getComments(post, banned_words_for_comments)
            if check_date_num ==  1:
                
                dict["Post Title"].append("RECENT " + post.title)
                dict["Comments"].append(comments)
            elif check_date_num == 0:

                dict["Post Title"].append(post.title)
                dict["Comments"].append(comments)
       
            counter += 1
    return dict

# Filtering posts
def filterPost(post, banned_words, mod_name):
    # combine title and body of post
    post_text = post.title + " " + post.selftext
    for word in banned_words:
        if post_text.lower().find(word) >= 0: # if can find
            #print(word)
            return False
    if post_text.find(mod_name):
        return True
    else:
        print("no mod name")
        return False
        

# Filtering comments
def filterComment(comment, banned_words):
    comment_body = comment.body
    for word in banned_words:
        if comment_body.lower().find(word) >= 0:
            return False
    return True

# Function to get comments of a post
def getComments(post, banned_words):
    store = []
    post.comments.replace_more(limit=None)
    comments = post.comments.list()
    for comment in comments:
         # comment requirements : >=5 words, >3 upvote, 
        if len(comment.body.split(" "))>=7 and filterComment(comment, banned_words):
            store.append(comment.body)
    #print(store)
    return store

def scrape_title(mod, subreddit, n):
    lst = []
    counter = 1
    for post in subreddit.search(mod):
        if counter <= n:
            lst.append(post.created_utc)
        counter += 1
    return lst

# Main function
if __name__ == "__main__":
    #clearCSV()
    #print(scrape_n_posts("cs2030", 5))
    #print(scrape_posts("ec1101e", nus_sub, 3))
    print(scrape_posts("cs2030", nus_sub, 3))

