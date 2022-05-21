import datetime
from tabnanny import check
from numpy import true_divide
import praw
import pandas as pd
import re
from requests import post
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer



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
def find_top_five(subreddit):
    for post in subreddit.hot(limit=5):
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

# testing function
def testing(subreddit):
    for post in subreddit.hot(limit=5):
        time = post.created
    
        print(datetime.datetime.fromtimestamp(time))

keywords = ["mods", "modules"]
modList = ["CS", "BT", "GE", "IS"]  #May need the prefix of all mods?

# Filtering function
def filterPost(dict, word, postID, dictKey):
    if postID not in dict[dictKey]:
        if word in keywords or checkMods(modList, word):
            return True

    return False


# Scraping posts while filtering for mods , returns a dataFrame
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

# Function to get comments of a post
def getComments(post):
    commentsDict = {"Comment Text": [], "Comment ID": [], "Comment Score": [], "Time Posted": []
              }
    comments = post.comments.list()
    for comment in comments:
        commentsDict["Comment Text"].append(comment.body)
        commentsDict["Comment ID"].append(comment.id)
        commentsDict["Comment Score"].append(comment.score)
        commentsDict["Time Posted"].append(datetime.datetime.fromtimestamp(comment.created))
    
    comments = pd.DataFrame(commentsDict)
    return comments
    

# Function to check module name/wildcard 

# def checkMods(modList, word):
#     for mod in modList:
#         modString = mod + ".+"
#         if bool(re.search(modString, word)):
#             return True
#     return False

def checkMods(modList, word):
    for mod in modList:
        modString = mod + "...."
        temp = re.compile(modString) 
        if bool(temp.search(word)):
            return True
        else:
            continue
    return False

# Function for sentiment analysis (TextBlob -> pre trained)
def sentimentAnalysis(string):
    blob = TextBlob(string)
    sentiment = blob.sentiment.polarity
    return sentiment

# Function to scrape posts and give sentiment score based on title 
def postSentiment(subreddit, limitNum, analysisFunc):
    modPosts_dict = {"Title": [], "Post Text": [], "Score": [], "ID":[],
              "Sentimental Score": [], "Post URL": []
              }
    for post in subreddit.hot(limit=limitNum):
        for word in post.title.split(" "):  #for each word in the post title(its type is list)
            if filterPost(modPosts_dict, word, post.id, "ID"):
                
                sentiment = analysisFunc(post.selftext)

                modPosts_dict["Title"].append(post.title)
                modPosts_dict["Post Text"].append(post.selftext)
                modPosts_dict["Score"].append(post.score)
                modPosts_dict["Sentimental Score"].append(sentiment)
                modPosts_dict["Post URL"].append(post.url)
                modPosts_dict["ID"].append(post.id)

    posts = pd.DataFrame(modPosts_dict)
    return posts

# Main function
if __name__ == "__main__":
    #find_top_five(nus_sub)
    #print(scrapeModPosts(nus_sub, 200))
    print(postSentiment(nus_sub, 200, sentimentAnalysis))

    
    
