# Enter Keys and Tokens here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# A function that can be called to get a specific key/token stored above
def get_key(key):
    return {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret
    }[key]
