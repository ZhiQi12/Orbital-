import praw
import pandas as pd
#from prawcore.exceptions import PrawcoreException
'''
reddit_read_only = praw.Reddit(client_id="7YGwTiuX_umf-SB_dqOUQA",         # your client id
                               client_secret="vJ7RrDCUYyS0xVd1Yv_hDVyGORd4nA",      # your client secret
                               user_agent="scrapingNUS",
                               username="ice_cream_12",
                               password="ZHIQI2024#zq")        # your user agent
'''
reddit_read_only = praw.Reddit(client_id="HJFREmWRT9QTnbohyZup6w",         # your client id
                               client_secret="S__YD99jhRGHnwWjzMFZTDlQeT18RA",      # your client secret
                               user_agent="Orbital")        # your user agent
subreddit = reddit_read_only.subreddit("nus")

print("Display Name:", subreddit.display_name)
print("Title:", subreddit.title)
print("Description:", subreddit.description)
print("POST")
for post in subreddit.hot(limit=5):
    print(post.title)
    print()
    print("Post")



    


