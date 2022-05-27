# MODeRATE 

MODeRATE is a web app which generates sentimental score for NUS modules based on reviews scraped from Reddit and NUSMODS. 

## Description 

MODeRATE is a web application which consists of web scraping and sentimental analysis components. Web scraping involves extracting information from a website. Sentimental analysis involves the use of algorithms to classify text to determine whether data is positive, negative or neutral. 

In this project, information such as reviews and comments are scraped from Reddit and NUSMODS. They are analysed by a custom made model which is trained on Reddit and NUSMODS datasets. The model produces a sentimental score for each review parsed into it. Factors that affect the sentimental score include date of post, number of upvotes, etc. This refines the sentimental score based on real time data.  
 

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