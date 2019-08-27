import uuid

import json
import heapq
from datetime import datetime

from models import db


class Tweet():

    def __init__(self, id=None, tweet=None, user_name=None, title=None, body=None):
        """

        :param id:
        :param tweet:
        :param user_name:
        :param title:
        :param body:
        """
        if not tweet:
            self.user_name = user_name  # 50 chars
            self.title = title  # 100 chars
            self.body = body  # 140 chars
            self.retweet = None  # 8 bytes

        else:
            self.user_name = tweet.user_name  # 50 chars
            self.title = tweet.title  # 100 chars
            self.body = tweet.body  # 140 chars
            self.retweet = tweet  # 8 bytes

        self.id = id if id else uuid.uuid4().hex
        self.created_at = str(datetime.now())
        self.count_retweet = 0

    def increase_counter(self):
        retweet = self.retweet  # type: Tweet
        while retweet is not None:
            tw = Tweet.get(retweet)
            tw.count_retweet += 1
            print("Increase counter for %s" % tw.id)
            tw.save(write_aof=False)
            retweet = tw.retweet

    def repost(self, tweet):
        """

        :param Tweet tweet:
        :return:
        """
        new_tweet = Tweet(tweet=tweet)
        tweet.increase_counter()

    @property
    def __dict__(self):
        return {
            'user_name': self.user_name,
            'title': self.title,
            'body': self.body,
            'retweet': self.retweet,
            'count_retweet': self.count_retweet,
            'id': self.id,
            'created_at': self.created_at
        }

    @classmethod
    def load_json(cls, tweet_json):

        tw = Tweet()
        tw.title = tweet_json.get('title')
        tw.user_name = tweet_json.get('user_name', 'anonymous')
        tw.body = tweet_json.get('body')
        tw.id = tweet_json.get('id', uuid.uuid4().hex)
        tw.count_retweet = tweet_json.get('count_retweet', 0)
        tw.created_at = tweet_json.get('created_at', str(datetime.now()))
        tw.retweet = tweet_json.get('retweet')
        return tw

    @classmethod
    def post(cls, **kwargs):
        user_name = kwargs.get('user_name')
        title = kwargs.get('title')
        body = kwargs.get('body')

        tweet = cls(
            user_name=user_name,
            title=title,
            body=body,

        )
        db.set(tweet.id, tweet)

    @classmethod
    def get(cls, id):
        tw = db.get(id)
        if tw:
            tweet_json = json.loads(tw)
        else:
            tweet_json = {}
        return cls.load_json(tweet_json)

    def save(self, write_aof=True):

        tweet_json = json.dumps(self.__dict__)

        db.set(self.id, tweet_json)
        if write_aof:
            db.bgrewriteaof()


    @staticmethod
    def simple_sort():
        json_data = []
        for key in db.scan_iter():
            json_data += [Tweet.load_json(json.loads(db.get(key))).__dict__]

        return heapq.nlargest(10, json_data, key=lambda data: data['count_retweet'])

    @classmethod
    def get_all(cls):
        print(db.sort(db.keys()))
