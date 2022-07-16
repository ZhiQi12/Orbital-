import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

# Setting up browser
website = 'https://nusmods.com/modules?sem[0]=1&sem[1]=2&sem[2]=3&sem[3]=4'

# Setting up browser
def getBrowser():
    ser = Service("./chromedriver")
    opt = webdriver.ChromeOptions()

    # Configuring to remove usb warning
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=ser, options=opt)
    return browser


def findMod(module):
    browser = getBrowser()
    website = 'https://nusmods.com/modules/' + module
    
    # go to NUSMODS website
    browser.get(website)
    
    #check if the mod exists by checking if the page has 404 error shown
    try:
        # Error shown, 404 (no mods)
        WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/main/div/p')))
        print("mod does not exist")
        return False
        
    except:
        # Mod exists
        print("mod exist")
        return browser
    
# Check if the module has more than 0 reviews    
def checkReviewCount(browser):
    # If mod does not exist
    if browser == False:
        return None

    #WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/main/div/div/aside/div[2]/div/nav/ul/li[4]/a/span/span[2]')))
    value = browser.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[1]/main/div/div/aside/div[2]/div/nav/ul/li[4]/a/span/span[2]').text
    print(int(value))
    if int(value) > 0:
        return True
    else:
        return False
        
def scrapeReviews(browser):
    # If mod does not exist    
    if browser == False:
        return None
    
    else:
        # if reviews > 0
        if checkReviewCount(browser):
            iframe = browser.find_elements(by=By.TAG_NAME, value='iframe')         
            browser.switch_to.frame(iframe[0])
            #browser.implicitly_wait(5)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'post')))

            posts = browser.find_elements(by=By.CLASS_NAME, value='post')
            #print(dateOfPost.text)
            postList = []
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
            counter = 1
            for post in posts: 
                #dateOfPost = browser.find_elements(EC.presence_of_all_elements_located((By.CLASS_NAME, 'time-ago')))
                
                #print(dateOfPost.text)
                #WebDriverWait()
                try:
                    #print("try")
                    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'see-more')))
                    seeMore = post.find_element(by=By.CLASS_NAME, value='see-more')
                    seeMore.click()
                    browser.implicitly_wait(3)
                except:
                    #Eprint("except")
                    print("no see-more option")
                    print(counter)
                    
                    continue
                finally:
                    counter += 1
                    #browser.implicitly_wait(5)
                    #print("finally")
                    WebDriverWait(browser, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
                    #browser.implicitly_wait(3)
                    postMsg = post.find_element(by=By.CLASS_NAME, value='post-message')
                    postList.append(postMsg.text) 
        else:
            return None
        
        return (postList)

def addCommentsToCSV(comments):
    with open('./comments.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        for comment in comments:
            writer.writerow([comment])

def clearCSV():
    # Truncates the csv file
    f = open('./comments.csv', 'w+')
    f.close()

if __name__ == '__main__':
    browser = findMod("cs1010")
    print(scrapeReviews(browser))
