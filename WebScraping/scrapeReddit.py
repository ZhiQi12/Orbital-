import datetime
from tabnanny import check
from numpy import true_divide
import praw
import pandas as pd
import re
from requests import post
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

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

# # Display posts' info
# def displayPostInfo(post, dict):
#     # dict = {"Title": [], "Post Text": [], "Score": [],
#     #           "Total Comments": [], "Post URL": [], "Time Posted": [], "ID": []
#     #         }
#     dict["Title"].append(post.title)
#     dict["Post Text"].append(post.selftext)
#     dict["Score"].append(post.score)
#     dict["Total Comments"].append(post.num_comments)
#     dict["Post URL"].append(post.url)
#     dict["Time Posted"].append(datetime.datetime.fromtimestamp(post.created))
#     dict["ID"].append(post.id)
    
#     return dict


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

def checkMods(modList, word):
    for mod in modList:
        modString = mod + "...."
        temp = re.compile(modString) 
        if bool(temp.search(word)):
            return True
        else:
            continue
    return False



# Main function
if __name__ == "__main__":
     print(scrapeModPosts(nus_sub, 200))
    


