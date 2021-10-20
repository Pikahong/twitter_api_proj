
users_profile = '''
    CREATE TABLE IF NOT EXISTS users_profile (
        user_id INTEGER NOT NULL,
        screen_name NVARCHAR(32),
        name NVARCHAR(32),
        location NVARCHAR(256),
        description NVARCHAR(256),
        followers_count INTEGER,
        friends_count INTEGER,
        statuses_count INTEGER,
        CONSTRAINT pk_user_id PRIMARY KEY (user_id)
    );
'''
tweets = '''
    CREATE TABLE IF NOT EXISTS tweets (
        tweet_id NOT NULL,
        user_id INTEGER NOT NULL,
        screen_name NVARCHAR(32),
        created_at DATETIME,
        body NVARCHAR(256),
        favorite_count INTEGER,
        retweet_screen_name NVARCHAR(32),
        CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
    );
'''

tables_schema = [users_profile, tweets]

# CONSTRAINT pk_tweet_id PRIMARY KEY (tweet_id),