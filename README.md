# TwitterProject

reference
https://towardsdatascience.com/twitter-data-collection-tutorial-using-python-3267d7cfa93e

# Load Twitter API secrets from an external JSON file

secrets = json.loads(open(path + 'secrets.json').read())

api_key = secrets['api_key']

api_secret_key = secrets['api_secret_key']

access_token = secrets['access_token']

access_token_secret = secrets['access_token_secret']

# Connect to Twitter API using the secrets

auth = tweepy.OAuthHandler(api_key, api_secret_key)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Helper function to get all tweets of a specified user

# NOTE:This method only allows access to the most recent 3200 tweets

# Source: https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name):
  # initialize a list to hold all the Tweets
  alltweets = []
  # make initial request for most recent tweets 
  # (200 is the maximum allowed count)
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
  # save most recent tweets
  alltweets.extend(new_tweets)
  # save the id of the oldest tweet less one to avoid duplication
  oldest = alltweets[-1].id - 1
  # keep grabbing tweets until there are no tweets left
  while len(new_tweets) > 0:
  
    print("getting tweets before %s" % (oldest))
  
  # all subsequent requests use the max_id param to prevent
  
  # duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
  
  # save most recent tweets
    alltweets.extend(new_tweets)
  
  # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
  
  print("...%s tweets downloaded so far" % (len(alltweets)))
  
  ### END OF WHILE LOOP ###
  
  # transform the tweepy tweets into a 2D array that will 
  
  # populate the csv
  outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count,tweet.in_reply_to_screen_name, tweet.retweeted] for tweet in alltweets]
  
  # write the csv
  
  with open(path + '%s_tweets.csv' % screen_name, 'w') as f:
  
  writer = csv.writer(f)
  
  writer.writerow(["id","created_at","text","likes","in reply to","retweeted"])
  
  writer.writerows(outtweets)
  
  pass
