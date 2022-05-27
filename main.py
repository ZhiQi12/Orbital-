from sentimentAnalysis import *
from scrapeReddit import *
from scrapeNUSMODS import *

# if __name__ == "__main__":
    #find_top_five(nus_sub)
    #print(scrapeModPosts(nus_sub, 200))
    #print(postSentiment(nus_sub, 200, sentAnalysis))
browser = findMod("CS1050")
print(scrapeReviews(browser))