import praw
import config

api_id = config.api_id[:-1]
api_secret = config.api_secret;

reddit = praw.Reddit(client_id = api_id,
                     client_secret = api_secret,
                     user_agent='<console:reddit_bot:0.0.1')

#TO-DO: Parse posts from time/date with certain inputs, ex what countries we parse

#================================
listOfPosts = [reddit.subreddit("coronavirus")(limit=1)]#getPostSomehow(), TO-DO
#================================

numPosts = 0 #for daily score breakdown

for post in listOfPosts:
  peoplePosted = [] #keep track of UNIQUE posters

  if post.author not in peoplePosted: #if not in list, add to day count
    numPosts = numPosts + 1

  peoplePosted.append(post.author)

  postName = post.name #title of post
  postScore = post.score #karma on the posts
  postURL = post.url #url the post links to
  postNumComments = post.num_comments #number of comments in the post
  postComments = post.comments(limit=5) #provides list of comments
  #==============================
  postSentiment = 0 #TODO
  #==============================


