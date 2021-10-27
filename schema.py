
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

followers = '''
    CREATE TABLE IF NOT EXISTS followers (
        follower_screen_name NVARCHAR(32) NOT NULL,
        user_id INTEGER NOT NULL,
        screen_name NVARCHAR(32),
        name NVARCHAR(32),
        location NVARCHAR(256),
        description NVARCHAR(256),
        followers_count INTEGER,
        friends_count INTEGER,
        statuses_count INTEGER,
        CONSTRAINT pk_follower PRIMARY KEY (follower_screen_name, user_id),
        CONSTRAINT fk_friends_following_screen_name FOREIGN KEY (follower_screen_name) REFERENCES users_profile(screen_name)
    );
'''

friends = '''
    CREATE TABLE IF NOT EXISTS friends (
        following_screen_name NVARCHAR(32) NOT NULL,
        user_id INTEGER NOT NULL,
        screen_name NVARCHAR(32),
        name NVARCHAR(32),
        location NVARCHAR(256),
        description NVARCHAR(256),
        followers_count INTEGER,
        friends_count INTEGER,
        statuses_count INTEGER,
        CONSTRAINT pk_follower PRIMARY KEY (following_screen_name, user_id),
        CONSTRAINT fk_friends_following_screen_name FOREIGN KEY (following_screen_name) REFERENCES users_profile(screen_name)
    );
'''

tweets = '''
    CREATE TABLE IF NOT EXISTS tweets (
        created_at DATETIME NOT NULL,
        tweet_id INTEGER NOT NULL,
        tweet_user_id INTEGER NOT NULL,
        screen_name NVARCHAR(32),
        retweet_created_at DATETIME,
        body NVARCHAR(256),
        favorite_count INTEGER,
        retweet_count INTEGER,
        retweet_screen_name NVARCHAR(32),
        CONSTRAINT pk_tweet PRIMARY KEY (created_at, tweet_id),
        CONSTRAINT fk_tweets_screen_name FOREIGN KEY (screen_name) REFERENCES users_profile(screen_name)
    );
'''

tables_schema = [users_profile, followers, friends, tweets]