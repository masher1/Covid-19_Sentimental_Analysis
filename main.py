import praw
import config
import pandas as pd
import requests
import json
import csv
import time
import datetime

# Global Variables
subStats = {}
small_data = []


def getPushshiftData(query, after, before):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit=coronavirus'
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def collectSubData(subm):
    subData = list()  # list to store data points
    title = subm['title']
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

    subData.append((sub_id, title, body, url, created, flair))
    subStats[sub_id] = subData

#================================Malkiel
#Unix Time: https://www.epochconverter.com/


#Upload data to a CSV file
def updateSubs_file():
    upload_count = 0
    ts = time.time()
    readable_time = datetime.datetime.fromtimestamp(ts).isoformat()
    filename = "DataCollection_" + query + ".csv"
    file = filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID", "Title", "Body", "Url", "Publish Date", "Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count += 1

        # for sub in subStats:
        #     for items in range(len(subStats[sub])):
        #         a.writerow(subStats[sub][items])
        #         upload_count += 1

        # for sub in range(len(small_data)):
        #     for items in range(len(small_data[sub])):
        #         a.writerow(small_data[sub][items])
        #         #a.writerow(subStats[sub][0])
        #         upload_count += 1
        #     a.writerow("")
        #     a.writerow("")
        print(str(upload_count) + " submissions have been uploaded")


if __name__ == '__main__':
    api_id = config.api_id
    api_secret = config.api_secret;

    reddit = praw.Reddit(client_id=api_id,
                         client_secret=api_secret,
                         user_agent='<console:reddit_bot:0.0.1')

    # Parse posts from time/date with certain inputs, ex what countries we parse
    # https://api.pushshift.io/reddit/search/submission/?subreddit=coronavirus&sort_type=created_utc&size=500&after=90d&before=20d
    query = "Italy"  # Country Name
    weeks = [1580515200, 1581120000, 1581724800, 1582329600, 1582934400, 1583539200, 1584144000, 1584748800, 1585353600, 1585958400, 1586563200] #Feb - Early Apr
    weekNum = 0
    big_data = []
    while (weekNum < len(weeks)-1):
        data = getPushshiftData(query, weeks[weekNum], weeks[weekNum+1])
        print("Number of submissions for week #" + str(weekNum+1) + ": " + str(len(data)))
        big_data.append(data)
        for submissions in data:
            collectSubData(submissions)
        weekNum += 1

    print("Number of weeks gathered in total: " + str(len(big_data)))
    small_data = big_data
    positive = ["recover","decline","vaccine","antibody","praise", "cases fall","lowest"]
    negative = ["death","test positive","close","shut down","lost","die","late","decease","highest"] 

    sentimentScores = []

    iterateNum = 0
    sentimentScore = 0.0

    while big_data:
        sentimentQuantity = len(big_data[iterateNum])
        sentimentScores = sentimentQuantity
        iterateNum += 1
        if (iterateNum >= len(big_data) - 1):
            break

    iterateNum = 0

    #while (iterateNum < len(big_data[iterateNum]) - 1):
    # for week_data in big_data[iterateNum]:
    #     for submission in week_data:
    #             title = submission['title']
    #             #TODO change the sentiment analysis structure
    #             if any(word in title for word in positive): #gets score for positive title
    #               sentimentScore += 1.0
    #             if any(word in title for word in negative): #gets score for negative title
    #               sentimentScore -= 1.0

        # Calls getPushshiftData() with the created date of the last submission
        #print("i am length" + str(len(big_data[iterateNum])))
        # print(str(datetime.datetime.fromtimestamp(big_data[iterateNum][-1]['created_utc'])))
        # after = big_data[iterateNum][-1]['created_utc']
        # before = big_data[iterateNum][-1]['created_utc']
        # data = getPushshiftData(query, after, before)
        # #big_data.append(data)
        # iterateNum += 1

    sentimentScore = sentimentScore / sentimentQuantity
    print("Score: "+str(sentimentScore))
    count = sum([len(listElem) for listElem in small_data])
    print(str(count) + " submissions have been added to list")

    updateSubs_file()