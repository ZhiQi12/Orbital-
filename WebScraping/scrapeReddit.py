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

#Print display_name, title, description (info of subreddit)
def get_subredditInfo(subreddit):
    print(subreddit.display_name)
    print(subreddit.title)
    print(subreddit.description)

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

###################################################################################################################################################
banned_words = ["telegram", "textbook","textbooks", "tele", "chats","grp", "group","chat","modreg", "internship", "notes", "bid", "bidding"]
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
    #banned_words = ["telegram", "textbooks", "tele", "chats"]
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
                # elif check_date_num == 0 and post.score >= 5:  
                    
                #     dict["Post Title"].append(post.title)
                #     dict["Comments"].append(comments)
        
                #top_3.extend(commentTuple[1])
       
                    counter += 1
    # for lst in dict["Comments"]:
    #     final += lst
    
    score_list = dict["Score"]
    new_score_list = list(enumerate(score_list))
    new_score_list = sorted(new_score_list, key = lambda x : x[1], reverse=True)
    for tuple in new_score_list:
        if len(top_3) < 3:
            index = tuple[0]
            top_3.append(dict["Comments"][index])
        else:
            break
    print(new_score_list)
    print(top_3)
    return dict["Comments"]

# Filtering posts
def filterPost(post, banned_words, mod_name):
    # combine title and body of post
    post_text = post.title + " " + post.selftext
    for word in banned_words:
        if post_text.lower().find(word) >= 0: # if can find
            print("got banned word")
            return False
    if post_text.lower().find(mod_name.lower()) >= 0:
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

def compareUpvotes(commentUpvote, postUpvote):
    if postUpvote >= 10:
        if commentUpvote >= 0.1*postUpvote:
            return True
        else:
            return False
    return True

# Function to get comments of a post
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
            #commentsDict["Score"].append(0)
            
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

    #print(commentsDict)
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
    #clearCSV()
    #print(scrape_n_posts("cs2030", 5))
    print(scrape_posts("cs1010e", nus_sub, 3))

