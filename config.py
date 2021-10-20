import tweepy
import logging
from credentials import get_key

# Create a logging object to print out messages by level
logger = logging.getLogger()

# Create a tweepy api object
def create_api():
    """ Read authentication credentials from keys,
    and create an tweepy api object """
    
    # Get the keys from credentials
    consumer_key = get_key('consumer_key')
    consumer_secret = get_key('consumer_secret')
    access_token = get_key('access_token')
    access_token_secret = get_key('access_token_secret')

    # OAuth authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Verify the credentials
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error('Error during authentication', exc_info=True)
        raise e
    logger.info("Authentication OK, API created")

    return api