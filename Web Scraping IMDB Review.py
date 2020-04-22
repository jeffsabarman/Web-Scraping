#Import Packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

#Scrap IMBD review from url link
ans = input("What movie do you want to watch?\nJust give me the URL from IMDB : ")
page = requests.get(ans)
soup = BeautifulSoup(page.content, "html.parser")
all = soup.find(id="main")
# review = all.find_all(class_ = "lister-item mode-detail imdb-user-review collapsable")
# print(review)
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
    print("NOT WATCH IT...")
print('Positive : ', sentiment1.count('positive'))
print('Negative : ', sentiment1.count('negative'))
print("")
print("According to TextBlob, you should :")
if sentiment2.count('positive') > sentiment2.count('negative'):
    print('WATCH IT!')
else:
    print("NOT WATCH IT...")
print('Positive : ', sentiment2.count('positive'))
print('Negative : ', sentiment2.count('negative'))

