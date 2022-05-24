from scrapeReddit import *

# Function for sentiment analysis (TextBlob -> pre trained)
def sentAnalysis(string):
    blob = TextBlob(string)
    sentiment = blob.sentiment.polarity
    return round(sentiment,2)

# Function to scrape posts and give sentiment score based on Post Text 
def postSentiment(subreddit, limitNum, analysisFunc):
    modPosts_dict = {"Title": [], "Post Text": [], "Score": [], "ID":[], "Post Object":[],
              "Sentimental Score": [], "Post URL": [], "Comment Sentiment": []
              }
    for post in subreddit.hot(limit=limitNum):
        for word in post.title.split(" "):  #for each word in the post title(its type is list)
            if filterPost(modPosts_dict, word, post.id, "ID"):
                
                sentimentPost = analysisFunc(post.selftext)
                sentimentComment = commentSentiment(post, analysisFunc)

                modPosts_dict["Title"].append(post.title)
                modPosts_dict["Post Text"].append(post.selftext)
                modPosts_dict["Score"].append(post.score)
                modPosts_dict["Sentimental Score"].append(sentimentPost)
                modPosts_dict["Post URL"].append(post.url)
                modPosts_dict["ID"].append(post.id)
                modPosts_dict["Post Object"].append(post)
                modPosts_dict["Comment Sentiment"].append(sentimentComment)


    posts = pd.DataFrame(modPosts_dict)
    return posts

def commentSentiment(post, analysisFunc):
    commentsDF = getComments(post)
    lst = []
    scores = []
    for comment in commentsDF["Comment Text"]:
        firstWord = comment.split(" ")[0]
        sentiment = analysisFunc(comment)
        scores.append(sentiment)
        scores.append(firstWord)
        lst.append(scores)
        scores = []
    return lst


if __name__ == "__main__":
    #find_top_five(nus_sub)
    #print(scrapeModPosts(nus_sub, 200))
    print(postSentiment(nus_sub, 100, sentAnalysis))


#problem = code crashes when limit is set high


