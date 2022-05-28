from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd


# Setting up browser
website = 'https://nusmods.com/modules?sem[0]=1&sem[1]=2&sem[2]=3&sem[3]=4'

# s = Service('.\chromedriver')
# opt = webdriver.ChromeOptions()

# # Configuring to remove usb warning
# opt.add_experimental_option('excludeSwitches', ['enable-logging'])

# driver = webdriver.Chrome(service=s, options=opt)

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
    #print(int(value))
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
            #browser.implicitly_wait(10)
            posts = browser.find_elements(by=By.CLASS_NAME, value='post')
            #print(len(posts))
            postList = []
            counter=1
            for post in posts:  
                browser.implicitly_wait(10)
                print(counter)        
                counter += 1   
                try:
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'see-more')))
                    seeMore = post.find_element(by=By.CLASS_NAME, value='see-more')
                    seeMore.click()
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
                    postMsg = post.find_element(by=By.CLASS_NAME, value='post-message')

                    postList.append(postMsg.text)
                    #print(postMsg.text)
                except:
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
                    postMsg = post.find_element(by=By.CLASS_NAME, value='post-message')
                    postList.append(postMsg.text) 
                    #print(postMsg.text)

               
        else:
            return None
        
        return (postList)

if __name__ == '__main__':
    browser = findMod("CS1010s")
    print(scrapeReviews(browser))
