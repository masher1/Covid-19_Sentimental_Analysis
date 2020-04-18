import praw
import config
import pandas as pd
import requests
import json
import csv
import time
import datetime

# Global Variables
subCount = 0
subStats = {}


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

        print(str(upload_count) + " submissions have been uploaded")



if __name__ == '__main__':
    api_id = config.api_id
    api_secret = config.api_secret;

    reddit = praw.Reddit(client_id=api_id,
                         client_secret=api_secret,
                         user_agent='<console:reddit_bot:0.0.1')

    # TO-DO: Parse posts from time/date with certain inputs, ex what countries we parse

    query = "Italy"  # Country Name
    after = "1580515200"  # Saturday, February 1, 2020 12:00:00 AM
    before = "1585699200"  # Wednesday, April 1, 2020 12:00:00 AM

    data = getPushshiftData(query, after, before)
    print(len(data))

    while len(data) > 0:
        for submission in data:
            collectSubData(submission)
            subCount += 1
        # Calls getPushshiftData() with the created date of the last submission
        print(len(data))
        print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
        data = getPushshiftData(query, after, before)

    print(str(len(subStats)) + " submissions have added to list")
    print("1st entry is:")
    print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
    print("Last entry is:")
    print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))

    updateSubs_file()
# for submission in reddit.subreddit('coronavirus').hot(limit=1000):
#     print(submission.title)
#     print("-----------------")

    #https://api.pushshift.io/reddit/search/submission/?subreddit=coronavirus&sort_type=created_utc&size=500&after=90d&before=20d
# listOfPosts = [reddit.subreddit("coronavirus")(limit=1)]#getPostSomehow(), TO-DO
#================================

# numPosts = 0 #for daily score breakdown
#
# for post in listOfPosts:
#   peoplePosted = [] #keep track of UNIQUE posters
#
#   if post.author not in peoplePosted: #if not in list, add to day count
#     numPosts = numPosts + 1
#
#   peoplePosted.append(post.author)
#
#   postName = post.name #title of post
#   postScore = post.score #karma on the posts
#   postURL = post.url #url the post links to
#   postNumComments = post.num_comments #number of comments in the post
#   postComments = post.comments(limit=5) #provides list of comments
#   #==============================
#   postSentiment = 0 #TODO
#   #==============================


