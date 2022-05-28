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
PATH = "C:/Users/Yan Rong/Documents/programming/Orbital/testsite/chromedriver.exe"

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

def scrape_n_posts(mod, n):
    driver = webdriver.Chrome(options = option, executable_path = PATH)
    driver.get("https://www.reddit.com/r/nus/")
    search = driver.find_element_by_id("header-search-bar")
    search.send_keys(mod)
    time.sleep(3)
    search.send_keys(Keys.RETURN)
    
    try:
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='QBfRw7Rj8UkxybFpX-USO']")))
    except:
        driver.close()
        return "Error"

    result = []
    scale = 0
    while scale < n:
        links = main.find_elements(By.XPATH,f'//a[contains(@href,"{mod.lower()}")]')
        links[scale * 2].click()
        driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.get(url)
        html =  BeautifulSoup(driver.page_source, "html.parser")
        comments = html.find_all("p",{"class":"_1qeIAgB0cPwnLhDF9XSiJM"})
        for comment in comments:
            result.append(comment.text)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        scale += 1
    driver.close()
    return result

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

def MODeRATE(MOD, n):
    return SIA_analyse_sent(scrape_n_posts(MOD, n))