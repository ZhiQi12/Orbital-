from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib import parse
import csv

# CONSTANTS ====================================================================
MODULE_PAGE = "https://nusmods.com/modules?sem[0]=1&sem[1]=2&sem[2]=3&sem[3]=4"

# ==============================================================================

class Mod:
    def __init__(self, code, title, link):
        self.code = code 
        self.title = title
        self.link = link
# ================================================================================================================

def getBrowser():
    ser = Service("./chromedriver")
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=ser, options=opt)
    return browser
# ================================================================================================================

def getMaxPages():
    browser = getBrowser()
    browser.get(MODULE_PAGE)

    LAST_PAGE_XPATH = '//*[@id="app"]/div/div[1]/main/div/div/div[1]/nav/ul/li[last()]/button'
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, LAST_PAGE_XPATH))).click()

    url = browser.current_url
    max_page_num =parse.parse_qs(parse.urlparse(url).query)['p'][0]
    browser.close()
    return max_page_num
# ================================================================================================================

def getPageMods(browser):
    # Wait for page to be hydrated
    first_mod_xpath = '//*[@id="app"]/div/div[1]/main/div/div/div[1]/div[2]/ul/li[1]/div/div[1]/header/h2/a'
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, first_mod_xpath)))

    # List to store mod info
    pageModsList = []

    # Find all mod headers
    all_mods = browser.find_elements(by=By.CLASS_NAME, value="ZaN0o9av")
    for mod in all_mods:
        anchorElem = mod.find_element(by=By.XPATH, value="a")
        
        modLink = anchorElem.get_attribute("href")
        modCode = anchorElem.find_element(by=By.XPATH, value="span[1]").text
        modTitle = anchorElem.find_element(by=By.XPATH, value="span[2]").text

        newMod = Mod(modCode, modTitle, modLink)
        pageModsList.append(newMod)
    
    return pageModsList
# ================================================================================================================
def addModsToCSV(modList):
    with open('./mods.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)

        for mod in modList:
            writer.writerow([mod.code, mod.title, mod.link])

def clearCSV():
    # Truncates the csv file
    f = open('./mods.csv', 'w+')
    f.close()

# ================================================================================================================

def getModList(max_page_num):
    browser = getBrowser()

    # Go through to the last page, and find mods
    i = 1
    while(i <= max_page_num):
        browser.get(MODULE_PAGE + f'&p={i}')
        pageModsList = getPageMods(browser)
        addModsToCSV(pageModsList)
        print(i)
        i += 1
# ================================================================================================================

if __name__ == '__main__':
    # Clears CSV file before scraping through again
    clearCSV()

    # Find last page number
    lastPageNum = getMaxPages()
    print(lastPageNum)
    # Loop through to get all mods
    getModList(int(lastPageNum))
