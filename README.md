# TwitterProject

#########reference
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
