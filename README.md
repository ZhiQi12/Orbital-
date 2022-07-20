## Level of Achievement: Apollo 11

![19e71a7ecb804111963590d0ee72f9d7 (1)](https://user-images.githubusercontent.com/74350301/175823931-8ac2c789-9121-4f13-8b4e-f4668dad3ae4.png)
# MODeRATE

MODeRATE is a web app which generates sentimental scores for NUS modules based on reviews scraped from Reddit. 

## Problem Statement
During ModReg, a NUS student may have a hard time deciding which modules to bid for in their upcoming semester of study. They may try to go to the NUS subReddit to search for reviews about the modules. In doing so, they may have a hard time finding out the general sentiment of the module given the numerous posts and comments that they would have to read through and compare. Such a process is also very time-consuming, inefficient and can be confusing for the student.

## Objective
To provide an efficient and effortless way for students to better understand the general sentiment of a module.

## Description 

MODeRATE is a web application that helps to determine the sentiment rating of a (NUS) module with the help of an artificial intelligent(AI) model. MODeRATE is made up of 2 components: web scraping and sentimental analysis. Web scraping involves extracting data from a website. Sentimental analysis involves the use of algorithms and AI models to classify text and determine whether a given input has a positive, negative or neutral sentiment associated with it. 

In this project, data such as text reviews, number of upvotes and date posted are scraped from the NUS subReddit. They are then passed through and analysed by our custom made AI model (using random forest regressor) trained on Reddit posts and submissions. The algrotihm filters out irrelevent comments based on certain criterias such as length of the post and nature of the post (a question or statement). The model then produces a sentiment score for each relevant review parsed into it. Factors such as date of post, number of upvotes, etc. help refine the sentiment score to account for relevance and credibility of the scraped posts. Additionally, to allow students to have an even better understanding of the general sentiment of the module, MODeRATE also generates the most relevant comments for users to view. An emotion chart is also provided for students to view the emotions associated with the module through the scraped posts.

With MODeRATE, NUS students can have a better gauge on the general sentiment of the module before they decide to bid during ModReg. It also allows the faculty to check on how well the module is doing over the semesters as our algorithm updates based on real-time data.


## Features

### Custom AI Model
* Transformers such as CountVectorizer and TFIDFTransformer
* Random Forest Regressor AI Model
* Trained on Reddit submissions dataset
* More accurate analysis than a pre-trained model

### Sentiment Rating
* Gives a score out of ten (Quantifiable)
* Easy to compare across different modules

### Top 3 comments
* Display the top 3 most relevant comments about the module
* Relevance determined by number of upvotes and date posted
* Acts as references for the user to better understand what others are saying about the module

### Emotion Chart
* A pie chart used to display the emotions associated with the reviews about the modules
* Displays for users to understand the breakdown of emotions from all the scraped reviews
	
### View Metrics
* Sorts and displays the top 3 highest-rated and most-searched module in MODeRATE.
* To show user which modules are the most popular in MODeRATE

## Design Principles

### Webscrapping
The primary function of the webscrapping component is used to extract relevant data from websites to be parsed into our artificial intelligent(AI) model for text analysis. The Python PRAW library, which is an exclusive webscrapping tool for Reddit, was used. A few other webscrapping tools and libraries such as Selenium and BeautifulSoup were also considered. However, PRAW yielded the best results in terms of time complexity.

#### Website choice
A small-scale survey was conducted to determine which websites students would go to to find reviews for modules. Namely, two particular websites were mentioned: NUSMODs and the NUS subReddit.

* NUSMODs
A significant portion of the module reviews were quite outdated (>3 years). Several students mentioned how such reviews were unreliable as many changes would have been made to the module by the time they were taking it. Hence, NUSMODs was not included as a data source for webscrapping in this project.

* NUS subReddit
Module reviews shown are rather recent (<2 years). New posts are made more frequently as compared to NUSMODs, hence the module reviews are more reliable. Some students pointed out an issue which is that some reviews show high degree of bias, seen by the use of certain high-intensity word phrases to describe the module. While some students prefer objective reviews, having a biased comment is also a way to show the general sentiment surrounding the module. Hence, the NUS subReddit was chosen to be a data source for webscrapping in this project.

#### Data scrapped
* Text comment - Primary component to use for sentiment analysis by the AI model. Short comments usually do not provide very constructive reviews about the modules. Hence, upon further testing, a minimum length of 8 words must be present in a text body for it to be considered relevant and be scrapped.

* Number of upvotes - A factor used to determine the relevance of a comment. A high number of upvotes can be used to indicate that a particular review resonated well with other users, hence its reliability.

* Date of post - Another factor used to determine the relevance of a comment. A newer post can indicate a 'fresher' and hence, a more reliable review as opposed to an older post. This is based on the assumption that fewer changes can happen to a module in a smaller span of time. However, it is still possible for a drastic change to occur over a single semester of study.

### Relevance Scoring System
The relevance scoring system(RSS) acts as an extension from the webscrapping component of this project. After the above data have been scrapped from Reddit, a score will be given to a post to help determine its relevance. Refer to the scoring system below:



### Artificial Intelligent(AI) Model
The primary function of the AI model was to recognise patterns in a text to determine the sentiment associated with it in the context of a module review. The method used here was the Bag-of-Words(BoW) approach to help convert texts from our dataset into numerical form used for anaysis.

#### Transformers
* Count Vectorizer
* Select-K-Best
* TFID Vectorizer

#### Machine Learning Alogrithm
Several machine learning algorithms were tested for their accuracy to determine which model was best suited for sentiment analysis in this case study.

### Integrated System Design

## Getting Started

### Dependencies

* Python 3.9+
* Google Chrome

### Libraries

* PRAW
* pandas
* NLTK
* scikit-learn
* Django
* pickle
* spaCy

### Installing
* Create and activate virtual environment

* Install Python Dependencies
```
pip install -r requirements.txt
```

### Changing path for files
* Navigate to folder fe -> moderate -> main.py, change the file path for line 15 such that it references the folder containing *WebScraping* folder.
* Navigate to folder fe -> moderate -> main.py, change the file path for line 58 such that it references the file location of *RFR_model.sav*.

### Operating on Django
* To run the web application using Django, navigate to the folder with *manage.py* file in command prompt and run:
```
python manage.py runserver
```
copy the URL provided in the command prompt:
```
http://127.0.0.1:8000/
```
paste it in a Google Chrome browser and press enter. The web application should now be running.

* To view the database storing the modules and issues:
1) Create an admin by navigating to the folder with *manage.py* file in command prompt and run:
```
python manage.py createsuperuser
```
2) Enter your desired username and press enter.
3) Enter your email address and press enter. This field can be left blank.
4) Enter your desired password and press enter.
5) Admin user is now created. With the web app running, enter the following URL:
```
http://127.0.0.1:8000/admin/
```	
6) Input the corresponding username and password. Press enter.
7) Database is now accessible.

## How To Use
1) Upon starting up the web application in a Google Chrome browser, you should be directed to the homepage. 
2) In the homepage, instructions are given on how to use MODeRATE.
3) Using the sidebar, click on *Find* which will navigate you to the search function.
4) Input the desired module code and press enter/click the submit button.
5) MODeRATE will display the sentiment rating, top 3 comments and emotion chart for the user to view.
6) If there is an issue, click the *Report Problem* button at the bottom right of the screen.
	* Enter the problem into the text box and click *Submit*.
	* From there, you can return to the homepage by clicking on the *Return to Home* button.
7) To use the View Metrics feature, click on *View* using the sidebar which will navigate you to the viewing menu.
8) Click on *Highest-Rated Mods* or *Most-Searched Mods* to view the respective metrics.
9) After done using the app, CTRL-BREAK in command prompt to close it.

### Flow Chart
<img width="3190" alt="flowchart" src="https://user-images.githubusercontent.com/74350301/175825096-75fdf0ea-309a-4070-844b-d1236cca35a7.png">



## Authors

Contributor names

* Chew Zhi Qi 
* Foo Yan Rong
