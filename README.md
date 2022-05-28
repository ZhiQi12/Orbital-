# MODeRATE 

MODeRATE is a web app which generates sentimental score for NUS modules based on reviews scraped from Reddit and NUSMODS. 

## Description 

MODeRATE is a web application which consists of web scraping and sentimental analysis components. Web scraping involves extracting information from a website. Sentimental analysis involves the use of algorithms to classify text to determine whether data is positive, negative or neutral. 

As there are many different kinds of reviews on Reddit and NUSMOD providing different sentiments for a module, a user who is trying to find out the general sentiment of the module may get easily confused after comparing all the different reviews. MODeRATE provides an algorithm to consolidate and compute all the different reviews before giving a final sentiment rating of the module. MODeRATE also provides a convenient way for the user to compare the general sentiments across different modules.

In this project, information such as reviews and comments are scraped from Reddit and NUSMODS. They are analysed by a custom made model which is trained on Reddit and NUSMODS datasets. The model produces a sentimental score for each review parsed into it. Factors that affect the sentimental score include date of post, number of upvotes, etc. This refines the sentimental score based on real time data.  

With MODeRATE, NUS students can have a better gauge on the general sentiment of the module before they decide to bid during ModReg. It also allows the faculty to check on how well the module is doing over the semesters as our algorithm updates based on real-time data.


## Features

### Model

* Detecting sarcasm
* Most commonly used words/phrases by students to describe modules
* Refine score to show weighted value of a review based on date of post, number of upvotes, etc

### Website

* Allows user to input a module code 
* Returns a sentimental score of the module
* Provide the most relevant reviews for students to view 
* Datebase to store the sentimental scores and most relevant reviews

## Getting Started

### Dependencies

* Python 3.9+
* Google Chrome

### Libraries

* Selenium
* BeautifulSoup
* Pandas
* NLTK
* Time
* Django 

### Installing
* Create and activate virtual environment

* Install Python Dependencies
```
pip install -r requirements.txt
```
* Install chrome driver for selenium scraping
* Unzip and place driver in project's root directory
	* [Link to Chrome Driver Download (Select based on chrome version)](https://chromedriver.chromium.org/downloads)


### Executing program
* Run main script
```
python main.py
```

## Authors

Contributors names

* Chew Zhi Qi 
* Foo Yan Rong