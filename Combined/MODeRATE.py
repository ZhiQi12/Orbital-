import nltk
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service

import spacy
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS

#reddit = praw.Reddit(client_id='m0T7JivawYEgBVsff5M08A',
#                     client_secret='PQC4K_w0Fjavpu2g4acaK8DnMhXZQg',
#                     user_agent='OrbAcct')

#mods = {}
#pattern = r"[A-Za-z][A-Za-z]\d\d\d\d"
#pattern = input("Input Mod: ")
#pattern = "CS1010S"
#nus = reddit.subreddit('nus')
#for submission in nus.new(limit=200):
#    search = re.search(pattern, submission.title)
#    if search:
#        mod = submission.title[search.start():search.end()]
#        if mod not in mods.keys():
#            mods[mod] = []
#        mods[mod].append((submission.title, [comment.body for comment in submission.comments]))
#print(mods)

#Selenium, BeautifulSoup
#PATH = "C:/Users/Yan Rong/Documents/programming/Orbital/testsite/chromedriver.exe"



# def scrape_n_posts(mod, n):
#     PATH = "C:\Orbital\Orbital_Moderate\chromedriver.exe"

#     option = Options()
#     option.add_argument("--disable-infobars")
#     option.add_argument("start-maximized")
#     option.add_argument("--disable-extensions")

#     # Pass the argument 1 to allow and 2 to block
#     option.add_experimental_option(
#     "prefs", {"profile.default_content_setting_values.notifications": 1})

#     driver = webdriver.Chrome(options = option, executable_path = PATH)
#     driver.get("https://www.reddit.com/r/nus/")
#     search = driver.find_element_by_id("header-search-bar")
#     search.send_keys(mod)
#     time.sleep(3)
#     search.send_keys(Keys.RETURN)
    
#     try:
#         main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='QBfRw7Rj8UkxybFpX-USO']")))
#     except:
#         driver.close()
#         return "Error"

#     result = []
#     scale = 0
#     while scale < n:
#         links = main.find_elements(By.XPATH,f'//a[contains(@href,"{mod.lower()}")]')
#         links[scale * 2].click()
#         driver.switch_to.window(driver.window_handles[1])
#         url = driver.current_url
#         driver.get(url)
#         html =  BeautifulSoup(driver.page_source, "html.parser")
#         comments = html.find_all("p",{"class":"_1qeIAgB0cPwnLhDF9XSiJM"})
#         for comment in comments:
#             result.append(comment.text)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         scale += 1
#     driver.close()
#     return result
PATH = "C:\Orbital\Orbital_Moderate\chromedriver.exe"

def scrape_n_posts(mod, n):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
    driver = webdriver.Chrome(options = option, executable_path = PATH)
    driver.get("https://www.reddit.com/r/nus/")
    search = driver.find_element(by=By.ID, value = 'header-search-bar' )
    #search = driver.find_element_by_id("header-search-bar")
    search.send_keys(mod)
    time.sleep(3)
    search.send_keys(Keys.RETURN)

    result = []
    scale = 0
    inturl = driver.current_url
    while scale < n:
        try:
            main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='QBfRw7Rj8UkxybFpX-USO']")))
        except:
            driver.close()
            return ["Error"]
        links = main.find_elements(By.XPATH,f'//a[contains(@href,"{mod.lower()}")]')
        links[scale].click()
        #driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.get(url)
        html =  BeautifulSoup(driver.page_source, "html.parser")
        comments = html.find_all("p",{"class":"_1qeIAgB0cPwnLhDF9XSiJM"})
        for comment in comments:
            result.append(comment.text)
        #driver.close()
        #driver.switch_to.window(driver.window_handles[0])
        scale += 1
        driver.get(inturl)
    driver.close()
    return result

def most_relevant_comment(mod):
    # look at post title and filter out (telegram, textbooks, grp chats, internship, pyp, friends etc)
    # filter out upvote post < 5
    # comment requirements : >5 words, >3 upvote, 
    browser = getBrowser()
    browser.get("https://www.reddit.com/r/nus/")
    search = browser.find_element(by=By.ID, value = 'header-search-bar' )
    #search = driver.find_element_by_id("header-search-bar")
    search.send_keys(mod)
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    try:
        main = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='QBfRw7Rj8UkxybFpX-USO']")))
    except:
        browser.close()
        return ["Error"]

    store = []

    postTitles = main.find_elements(by=By.CLASS_NAME, value = "_eYtD2XCVieq6emjKBH3m")
    for title in postTitles:
        store.append(title.text)
    
    browser.close()

    return store


# Setting up browser
def getBrowser():
    ser = Service("./chromedriver")
    #opt = webdriver.ChromeOptions()
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1})
    # Configuring to remove usb warning
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=ser, options=option)
    return browser

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
    print(df["compound"].mean())
    return df

#TextBlob
from textblob import TextBlob

def TB_analyse_sent(comments):
    results = []
    for comment in comments:
        entry = {}
        tb = TextBlob(comment)
        #Subjectivity
        entry["Score"] = tb.polarity
        entry["Comment"] = comment
        results.append(entry)
        
    df = pd.DataFrame.from_records(results)
    print(df["Score"].mean())
    return df


def counter(ls):
    nlp = spacy.load("en_core_web_sm")

    ls = " ".join(ls)
    ls = [token.text for token in nlp(ls) if (not nlp.vocab[token.text].is_stop) & (token.pos_ not in ["PUNCT", "SPACE", "SYM"])]
    word_freq = Counter(ls)
    return word_freq 

#print(counter(scrape_n_posts("GES1035", 8)).most_common(10))
#print(scrape_n_posts('cs1010s', 5))
print(most_relevant_comment("cs1010s"))