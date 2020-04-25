#Import Packages
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import time

movie = input("What movie or tv shows do you want to watch? : ")

#Set the web browser
driver = webdriver.Chrome(executable_path=r"C:\Users\asus liberty\PycharmProjects\Web Scraping\Browser\chromedriver.exe")

#Go to Google
driver.get("https://www.google.com/")

#Enter the keyword
driver.find_element_by_name("q").send_keys(movie + " imdb")
time.sleep(1)

#Click the google search button
driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
time.sleep(1)

#Click the link
driver.implicitly_wait(20)
driver.find_element_by_class_name("r").click()
driver.implicitly_wait(20)

#Click the user reviews
driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[5]/div[1]/div/div/div[1]/div[1]/div[1]/a[3]").click()

#Scrap IMBD review
ans = driver.current_url
page = requests.get(ans)
soup = BeautifulSoup(page.content, "html.parser")
all = soup.find(id="main")

#Get the title of the movie
all = soup.find(id="main")
parent = all.find(class_ ="parent")
name = parent.find(itemprop = "name")
url = name.find(itemprop = 'url')
film_title = url.get_text()

#Get the title of the review
title_rev = all.select(".title")
title = [t.get_text().replace("\n", "") for t in title_rev]

#Get the review
review_rev = all.select(".content .text")
review = [r.get_text() for r in review_rev]

#Make it into dataframe
table_review = pd.DataFrame({
    "Title" : title,
    "Review" : review
})

#Sentiment Analysis

#Vadersentiment
analyser = SentimentIntensityAnalyzer()
sentiment1 = []
sentiment2 = []

for rev in review:
    score1 = analyser.polarity_scores(rev)
    com_score = score1.get('compound')
    if com_score  >= 0.05:
        sentiment1.append('positive')
    elif com_score > -0.05 and com_score < 0.05:
        sentiment1.append('neutral')
    elif com_score <= -0.05:
        sentiment1.append('negative')

table_review['Sentiment Vader'] = sentiment1

#TextBlob
for rev in review:
    score2 = TextBlob(rev).sentiment.polarity
    if score2 >= 0:
        sentiment2.append('positive')
    else:
        sentiment2.append('negative')
print(f"The movie title is {film_title}")
print("")
print("According to vadersentiemnt, you should :")
if sentiment1.count('positive') > sentiment1.count('negative'):
    print('WATCH IT!')
else:
    print("DON'T WATCH IT...")
print('Positive : ', sentiment1.count('positive'))
print('Negative : ', sentiment1.count('negative'))
print("")
print("According to TextBlob, you should :")
if sentiment2.count('positive') > sentiment2.count('negative'):
    print('WATCH IT!')
else:
    print("DON'T WATCH IT...")
print('Positive : ', sentiment2.count('positive'))
print('Negative : ', sentiment2.count('negative'))

#Close the browser
driver.close()
