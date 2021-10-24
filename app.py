import sys
import re
import json
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
from collections import defaultdict
from config import create_api
from database import create_db

# Show all columns when printing dataframe objects
pd.set_option('display.max_columns', None)

# Create DB Engine and API Object
con = create_db(log=False)
api = create_api()


def get_all_tweets(screen_name):
    """ Get all tweets by screen_name. Max tweets up to 3250, retricted by Twitter """
    # tweet id can be repeated due to self-retweet. Can not set primary key to retweet_id
    # Create a empty dict with default empty list as values
    tweets = defaultdict(list)

    # status = tweet
    for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended", count=200).items():
        # When using extended mode with a Retweet,
        # the full_text attribute of the Status object may be truncated
        # with an ellipsis character instead of containing the full text of the Retweet
        # To get the full text of the Retweet, dive into 'retweeted_status'
        # Check if retweeted_status exisits
        is_retweet = hasattr(status, 'retweeted_status')
        # change the status root to retweeted_status
        tweets['screen_name'].append(status.user.screen_name)
        tweets['created_at'].append(
            datetime.strftime(status.created_at, '%Y-%m-%d'))
        if is_retweet:
            status = status.retweeted_status
            tweets['retweet_screen_name'].append(status.user.screen_name)
            tweets['retweet_created_at'].append(
                datetime.strftime(status.created_at, '%Y-%m-%d'))
        else:
            tweets['retweet_screen_name'].append(None)
            tweets['retweet_created_at'].append(None)

        tweets['tweet_id'].append(status.id)
        tweets['body'].append(status.full_text)
        tweets['user_id'].append(status.user.id)
        tweets['favorite_count'].append(status.favorite_count)
        tweets['retweet_count'].append(status.retweet_count)

    # Set primary key columns as index
    df = pd.DataFrame(tweets).set_index(['created_at', 'tweet_id'])
    # A temporary table for deleting the existing rows from tweets table
    df.to_sql('tweets_tmp', con, index=True, if_exists='replace')

    try:
        # delete rows that we are going to update
        con.execute(
            'DELETE FROM tweets WHERE (created_at, tweet_id) IN (SELECT created_at, tweet_id FROM tweets_tmp)')
        con.commit()

        # insert and update table
        df.to_sql('tweets', con, index=True, if_exists='append')
    except Exception as e:
        print(e)
        con.rollback()

    # dump a json file to inspect the context
    # with open('test.json', 'w') as fh:
    #     json_obj = json.dumps(test[1]._json, indent=4, sort_keys=True)
    #     fh.write(json_obj)

    # Save to a csv file for debugging
    print(df[['body', 'favorite_count']])
    df.to_csv('data.csv')


def get_users_profile(screen_name):
    """ Get user basic profiles by screen_name """
    users = defaultdict(list)
    user = api.get_user(screen_name=screen_name)
    users['user_id'].append(user.id)
    users['screen_name'].append(user.screen_name)
    users['name'].append(user.name)
    users['location'].append(user.location)
    users['description'].append(user.description)
    users['followers_count'].append(user.followers_count)
    users['friends_count'].append(user.friends_count)
    users['statuses_count'].append(user.statuses_count)

    # Set primary key column as index
    df = pd.DataFrame(users).set_index(['user_id'])
    # A temporary table for deleting the existing rows from tweets table
    df.to_sql('users_profile_tmp', con, index=True, if_exists='replace')

    try:
        # delete rows that we are going to update
        con.execute(
            'DELETE FROM users_profile WHERE user_id IN (SELECT user_id FROM users_profile_tmp)')
        con.commit()

        # insert and update table
        df.to_sql('users_profile', con, index=True, if_exists='append')
    except Exception as e:
        print(e)
        con.rollback()

    # with open('record.json', 'w') as fhandler:
    #     json.dump(user._json, fhandler)

    # import pprint
    # import inspect
    # inspect the method of 'user' object
    # pprint.pprint(inspect.getmembers(user, predicate=inspect.ismethod))
    # show only 20 followers
    # for follower in user.followers():
    #     print(follower.name)


# Read the predefined keywords from ./keywords.txt line by line and store into a list.
keywords = []
with open('keywords.txt', 'r', encoding="utf-8") as fh:
    keywords = [line.strip().lower() for line in fh]

# convert a list into a single sql command for filtering the keywords
sql_keywords = ' OR '.join(
    [f'body LIKE \'%{kw.strip().lower()}%\'' for kw in keywords])


# a helper function that extracts all the keywords from a tweet and store into a list
def _get_keywords(row):
    matched_keywords = []
    for kw in keywords:
        if kw in row.lower():
            matched_keywords.append(kw)
    return matched_keywords


def read_data(screen_name):
    """Read data(body) based on keywords"""

    sql = \
        f"""
        SELECT created_at, body FROM tweets
            WHERE UPPER(screen_name)=UPPER('{screen_name}')
            AND ({sql_keywords})
        """
    sql2 = f"SELECT * FROM tweets WHERE UPPER(screen_name)=UPPER('{screen_name}')"

    try:
        cur = con.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=['Date', 'Result'])
        df['Date'] = df['Date'].astype('datetime64')
        df['Keyword'] = df['Result'].apply(lambda row: _get_keywords(row))
        df.to_csv("READ.csv", index=False)
        print(df)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # implement a simple command line interface
    if len(sys.argv) == 3:
        args_str = ' '.join(sys.argv[1:])
        # Regex for matching the pattern : app.py [-utr] [screen_name]
        r = re.compile('^-(?P<options>[utr]+)\s+(?P<arg>\w+)$')
        m = r.match(args_str)
        # If there are matches
        if m is not None:
            args_dict = m.groupdict()
            # Get user profile
            # usage: python app.py -u [screen_name]
            if 'u' in args_dict['options']:
                get_users_profile(args_dict['arg'])

            # Get all tweets
            # usage: python app.py -t [screen_name]
            if 't' in args_dict['options']:
                get_all_tweets(args_dict['arg'])

            if 'r' in args_dict['options']:
                read_data(args_dict['arg'])
        else:
            print("""
                        Incorrect usage:
                        app.py [-utr] [screen_name]
                  """)

# Testing
# df = pd.read_csv('READ.csv')
# df['Date'] = df['Date'].astype('datetime64').dt.date
# from dateutil.relativedelta import relativedelta
# max_date = df['Date'].max()
# min_date = df['Date'].min()
# diff_date = max_date - min_date
# rdelta = relativedelta(max_date, min_date)

# total_month = rdelta.years * 12 + rdelta.months
# print(total_month)
# plt.hist(df.Date, bins=total_month)
# plt.xticks(fontsize=8)
# plt.show()

con.close()
