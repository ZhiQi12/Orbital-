import praw
import pandas as pd
import re
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

def addCommentsToCSV(comments):
    with open('./comments.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        for comment in comments:
            writer.writerow([comment])

def clearCSV():
    # Truncates the csv file
    f = open('./comments.csv', 'w+')
    f.close()

###################################################################################################################################################
banned_words = ["telegram", "textbook","textbooks", "tele", "chats","grp", "group","chat","modreg", "internship", "notes", "bid", "bidding"]
banned_words_for_comments = ["thank", "thanks", "?", "thx"]

def check_date(post): 
    date_posted = post.created_utc  # date posted
    today = time.time()  # today's time
    five_months = 13148715
    two_weeks = 1209600
    three_yrs = 94608000
    diff = float(today) - float(date_posted)
    if diff >= three_yrs:
        return -1  # don't scrape
    elif diff <= five_months:
        return 1   # scrape, don't need check upvote because post is recent (less than 5 months ago)
    else:
        return 0   #check upvote then can scrape


def scrape_posts(mod, subreddit, n):
    dict = {"Post Title": [], "Comments":[], "Score":[]}
    counter = 1
    top_3 = []
    for post in subreddit.search(mod):
        if counter <= n and filterPost(post, banned_words, mod):
            check_date_num = check_date(post)
            if check_date_num == -1 or post.num_comments == 0:  # if post is moren than 3 yrs old or got no comments, skip post
                continue
            else: 
                print(post.title)

                if check_date_num ==  1 or check_date_num == 0:
                    commentsDict = getComments(post, banned_words_for_comments)
                    dict["Post Title"].append(post.title)
                    dict["Comments"].extend(commentsDict["Body"])  # all relevant comments
                    dict["Score"].extend(commentsDict["Score"])
       
                    counter += 1
    
    score_list = dict["Score"]
    new_score_list = list(enumerate(score_list))
    new_score_list = sorted(new_score_list, key = lambda x : x[1], reverse=True)
    for tuple in new_score_list:
        if len(top_3) < 3:
            index = tuple[0]
            top_3.append(dict["Comments"][index])
        else:
            break

    return (dict["Comments"], top_3)
# Filtering posts
def filterPost(post, banned_words, mod_name):
    # combine title and body of post
    post_text = post.title + " " + post.selftext
    for word in banned_words:
        if post_text.lower().find(word) >= 0: # if can find
            #print("got banned word")
            return False
    if post_text.lower().find(mod_name.lower()) >= 0:
        return True
    else:
        #print("no mod name")
        return False
        

# Filtering comments
def filterComment(comment, banned_words):
    comment_body = comment.body
    for word in banned_words:
        if comment_body.lower().find(word) >= 0:
            return False
    return True

# Function to get all comments of a post and evaluate the score of each comment of a post
def getComments(post, banned_words):
    store = []
    commentsDict = {"Body": [], "Date Posted":[], "Upvote":[], "Score":[]}
    post.comments.replace_more(limit=None)
    # counter = 0
    post_upvote = post.score
    comments = post.comments.list()
    for comment in comments:
        if len(comment.body.split(" "))>=8 and filterComment(comment, banned_words):
            score = 0
            store.append(comment.body)
            comment_body = comment.body
            comment_date = comment.created_utc
            comment_upvote = comment.score
            commentsDict["Body"].append(comment_body)
            commentsDict["Date Posted"].append(comment_date)
            commentsDict["Upvote"].append(comment_upvote)
            
            # LENGTH SCORING
            if len(comment_body.split(" "))>= 200:
                score += 4
            elif len(comment_body.split(" ")) < 50:
                score += 0
            elif len(comment_body.split(" ")) < 100:
                score += 1
            elif len(comment_body.split(" ")) < 150:
                score += 2
            elif len(comment_body.split(" ")) < 200:
                score += 3
            
            # UPVOTE SCORING
            if comment_upvote >= post_upvote or comment_upvote >= 50:
                score += 3
            elif comment_upvote == 0:
                score += 0
            elif comment_upvote >= 20:
                score += 2
            else:
                if post_upvote >= 10:
                    if comment_upvote >= round(0.9*post_upvote):
                        score += 2
                    elif comment_upvote >= round(0.8*post_upvote):
                        score += 1
                else:
                    if comment_upvote <= 3:
                        score += 1
                    else:
                        score += 2
            
            # DATE SCORING
            today = time.time()
            four_months = 10368000
            one_yrs = 31536000
            diff = float(today) - float(comment_date)
            if diff <= four_months:
                score += 1

            commentsDict["Score"].append(score)

    return commentsDict

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
    print(scrape_posts("cs2030", nus_sub, 3))

