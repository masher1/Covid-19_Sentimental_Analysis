import config
import pandas as pd
import requests
import json
import csv
import time
import datetime
from textblob import TextBlob

# Global Variables
subStats = {}

#function used to collect the data from reddit given a country and start and end date
def getPushshiftData(query, after, before):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit=coronavirus'
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

#Function used to collect data for each submission
def collectSubData(subm):
    subData = list()  # list to store data points
    title = subm['title']
    titleBlob = TextBlob(title)
    sentiment_Score = titleBlob.sentiment.polarity
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    body = subm['selftext']
    created = datetime.datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    subData.append((sub_id, title, body, url, created, flair,sentiment_Score))
    subStats[sub_id] = subData

#Upload data to a CSV file
def updateSubs_file():
    upload_count = 0
    ts = time.time()
    readable_time = datetime.datetime.fromtimestamp(ts).isoformat()
    filename = "DataCollection_" + query + ".csv"
    file = filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID", "Title", "Body", "Url", "Publish Date", "Flair", "sentimentScore"]
        a.writerow(headers)
        for sub in subStats:
             a.writerow(subStats[sub][0])
             upload_count += 1
        print(str(upload_count) + " submissions have been uploaded")

#Main Method
if __name__ == '__main__':
    query = "Italy"  # Country Name
    weeks = [1580515200, 1581120000, 1581724800, 1582329600, 1582934400, 1583539200, 1584144000, 1584748800, 1585353600, 1585958400, 1586563200] #Feb - Early Apr
    weekNum = 0
    big_data = [] # will contain a list of lists of submissions 

    # make API call to get all post from each week and put them into bigData ==> list[list[Object{}],list[Object{}],...]
    while (weekNum < len(weeks)-1):
        data = getPushshiftData(query, weeks[weekNum], weeks[weekNum+1]) # will contain all submissions per week
        print("Number of submissions for week #" + str(weekNum+1) + ": " + str(len(data)))
        big_data.append(data)
        for submissions in data:
            collectSubData(submissions)
        weekNum += 1

    print("Number of weeks gathered in total: " + str(len(big_data)))
small    
    iterateNum = 0
   
    #Perform sentiment analysis on the title of each post
    while (iterateNum < len(big_data) - 1):
        for submission in big_data[iterateNum]:
            title = TextBlob(submission['title'])
            submission['sentimentScore'] = title.sentiment.polarity
        iterateNum += 1
    
    count = sum([len(listElem) for listElem in big_data])
    print(str(count) + " submissions have been added to list")
    
    #Update the .CSV file
    updateSubs_file()
