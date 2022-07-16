from django.test import TestCase
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
import time
import sys
import praw
sys.path.insert(1, 'C:/Orbital/Orbital_Moderate')
from WebScraping import scrapeReddit
# Create your tests here.
class MyTestCase(TestCase):

    def setUp(self):
        self.mod = "Mock mod"
        self.banned_words = ["banned"]
        # Mock Comment 1
        self.mock_comment1 = MagicMock()
        self.mock_comment1.body = "This comment has a banned word so there should only be 1 score"
        self.mock_comment1.created_utc = 1641006000  # 1/1/2022
        self.mock_comment1.score = 3
        #mock_comment1.replace_more.return_value = mock_comment1

        # Mock Comment 2
        self.mock_comment2 = MagicMock()
        self.mock_comment2.body = '''
        as a working professional, actually I'd argue for a non CS major looking to do SWE, CS2103 may help but in my opinion,
        there are actually more fundamental modules that's more important in actual practice (assuming the student already done CS2030/2040 or variants thereof)
        - for instance, CS2105 - networking knowledge is criminally underrated for a SWE - students don't know that don't know
        networking and/or operating systems will actually hit their limit fast as a technical person. don't get me wrong - the SWE course
        is great for getting exposure to projects, but there are actually more critical modules even as a SWE. the tendency however, is for students not to
        appreciate these content while they are learning it
        '''
        self.mock_comment2.created_utc = 1651374000  #1/5/2022
        self.mock_comment2.score = 9
        #mock_comment2.replace_more.return_value = mock_comment2

        # Mock Comment 3
        self.mock_comment3 = MagicMock()
        self.mock_comment3.body = '''
        Taking CS2030 and CS2040 this semester. I would say CS2040 helped me tremendously in passing OAs for SWE internships whereas CS2030 has been.
        Just my personal opinion though
        '''
        self.mock_comment3.created_utc = 1654052400  #1/6/2022
        self.mock_comment3.score = 12

        # Mock Comment 4
        self.mock_comment4 = MagicMock()
        self.mock_comment4.body = "This is the comment of mock comment 4"
        self.mock_comment4.created_utc = 1420052400  #1/1/2015
        self.mock_comment4.score = 0

        # Mock Comment 5
        self.mock_comment5 = MagicMock()
        self.mock_comment5.body = '''hello! i took this mod last sem and ur feelings are justified bc this mod was truly death for me. For some background, 
        I'm hopeless in math/data stuff lol, and DAO is all abt that so u can imagine....I tried to contribute most to the weekly group assignments, 
        and my group usually gets full marks/close to full marks. So those saved my final grade. For the project I wrote most of the report, excel analysis was
        done by my groupmates simply bc idk how to. If you really want to get a good grade (not S/U), I suggest going over topic by topic and redoing the questions
        in the lectures, group assignments, past year papers. Then consult on qns udk/don't understand. For finals I probably got 30% of the paper correct. Rest I 
        couldn't answer/half answered. In the end my final grade was C and I S/Ued it. So don't give up, this too shall pass haha
        '''
        self.mock_comment5.created_utc = 1654052400  #1/6/2022
        self.mock_comment5.score = 10

        #Mock Post 1
        self.mock_post1 = MagicMock()
        mock_commentsList1 = MagicMock(return_value=[self.mock_comment1, self.mock_comment2, self.mock_comment3, self.mock_comment4, self.mock_comment5], spec=praw.models.comment_forest.CommentForest)
        self.mock_post1.comments = mock_commentsList1
        self.mock_post1.comments.list.return_value = [self.mock_comment1, self.mock_comment2, self.mock_comment3, self.mock_comment4, self.mock_comment5]
        self.mock_post1.score = 5
        self.mock_post1.title = "Title for Mock Reddit Post 1 with Mock mod"
        self.mock_post1.selftext = "Selftext for Mock Reddit Post 1. This post has mock comment1,2,3,4,5."
        self.mock_post1.num_comments = len(self.mock_post1.comments.list.return_value)
        self.mock_post1.created_utc = 1654052400  #1/6/2022

        # Mock Post 2
        self.mock_post2 = MagicMock()
        mock_commentsList2 = MagicMock(return_value=[self.mock_comment3], spec=praw.models.comment_forest.CommentForest)
        self.mock_post2.comments = mock_commentsList2
        self.mock_post2.comments.list.return_value = [self.mock_comment3]
        self.mock_post2.score = 12      
        self.mock_post2.title = "Title for Mock Reddit Post 2"
        self.mock_post2.selftext = "Selftext for Mock Reddit Post 2. This post only has mock comment3"
        self.mock_post2.num_comments = len(self.mock_post2.comments.list.return_value)
        self.mock_post2.created_utc = 1641006000  # 1/1/2022
        pass

    def tearDown(self):
        pass

    def test_filterPost(self):
        print("test_filterPost")
        
        self.assertTrue(scrapeReddit.filterPost(self.mock_post1, self.banned_words, self.mod))
        self.assertFalse(scrapeReddit.filterPost(self.mock_post2, self.banned_words, self.mod))  # False as mock_post2 does not have mod name inside its title 

    def test_filterComment(self):
        print("test_filterComment")

        self.assertFalse(scrapeReddit.filterComment(self.mock_comment1, self.banned_words))  #False = banned words found
        self.assertTrue(scrapeReddit.filterComment(self.mock_comment2, self.banned_words))
        self.assertTrue(scrapeReddit.filterComment(self.mock_comment3, self.banned_words))


    def test_check_date(self):
        print("test_check_date")
        mock_post1 = MagicMock()
        mock_post1.created_utc = time.time() - 86400 # 1 day b4 today

        mock_post2 = MagicMock()
        mock_post2.created_utc = 1420052400  #1/1/2015

        self.assertEqual(scrapeReddit.check_date(self.mock_post1), 1)
        self.assertEqual(scrapeReddit.check_date(self.mock_post2), 0)
        self.assertEqual(scrapeReddit.check_date(mock_post1), 1)
        self.assertEqual(scrapeReddit.check_date(mock_post2), -1)
        
    
    @mock.patch('WebScraping.scrapeReddit.praw.Reddit', spec=praw.models.reddit.subreddit.Subreddit)
    def test_create_subreddit(self, mock_subreddit):
        print("test_create_subreddit")
        self.assertTrue(isinstance(mock_subreddit, praw.models.reddit.subreddit.Subreddit))

    def test_getComments(self):
        print("test_getComments")
        #print(scrapeReddit.getComments(self.mock_post1, self.banned_words))
        self.assertTrue(isinstance(scrapeReddit.getComments(self.mock_post1,self.banned_words), dict))
        self.assertTrue(isinstance(scrapeReddit.getComments(self.mock_post2,self.banned_words), dict))
        self.assertEqual(scrapeReddit.getComments(self.mock_post1, self.banned_words)["Score"], [6,4,0,7])
        self.assertEqual(scrapeReddit.getComments(self.mock_post2, self.banned_words)["Score"], [4])

    @mock.patch('WebScraping.scrapeReddit.praw.Reddit', spec=praw.models.reddit.subreddit.Subreddit)
    def test_scrape_posts(self, mock_subreddit):

        mock_subreddit.search.return_value = [self.mock_post1, self.mock_post2]   # Mock subreddit has 2 mock posts created in SetUp function above
        outcome = scrapeReddit.scrape_posts(self.mod, mock_subreddit, 3)
        #print(outcome)
        self.assertTrue(isinstance(outcome, tuple))
        self.assertEqual(len(outcome), 2)   # 2 lists in the tuple 
        self.assertEqual(type(outcome[0]), list) 



