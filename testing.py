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
reddit_read_only = praw.Reddit(client_id="7YGwTiuX_umf-SB_dqOUQA",         # your client id
                               client_secret="vJ7RrDCUYyS0xVd1Yv_hDVyGORd4nA",      # your client secret
                               user_agent="scrapingNUS")        # your user agent

subreddit = reddit_read_only.subreddit("redditdev")

print("Display Name:", subreddit.display_name)

print("Title:", subreddit.title)

    


