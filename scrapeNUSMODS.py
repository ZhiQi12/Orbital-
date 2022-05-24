from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#options = Options()

# Setting up
website = 'https://nusmods.com/modules?sem[0]=1&sem[1]=2&sem[2]=3&sem[3]=4'
path = 'C:\Orbital\Orbital_Moderate\chromedriver'
#driver = webdriver.Chrome(executable_path=path,chrome_options=options)
driver = webdriver.Chrome(path)
driver.get(website)



# Keying in module name 
def findingMod(module):
    #driver.find_element_by_xpath('//*[@id="search-box"]').send_keys(module)
    #driver.find_element_by_xpath('//*[@id="search-box"]').send_keys()
    driver.find_element_by_id("search-box").send_keys(module)
    driver.find_element_by_id("search-box").send_keys(Keys.RETURN)


#driver.quit()

findingMod("CS1010s")