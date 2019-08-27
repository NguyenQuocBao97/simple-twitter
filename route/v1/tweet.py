import json

import flask
from flask_restplus import Namespace
import flask_restplus as fr
import models as m
__DEFAULT_NAME__ = 'tweet'
tweet_ns = Namespace('', description='{} Resource Api'.format(__DEFAULT_NAME__.capitalize()))



class BaseResource(fr.Resource):

    def return_general(self, http_code, data=None):
        try:
            json.dumps(data)
        except:
            if not isinstance(data, str):
                data = str(data)

        return {
                   'data': data,
                   'http_code': http_code
               }, http_code



@tweet_ns.route('/tweet')
class TweetRoute(BaseResource):

    PostTweet = tweet_ns.model('PostModel', {
        'user_name': fr.fields.String(),
        'title': fr.fields.String(),
        'body': fr.fields.String(),
        # 'reweet': fr.fields.String(),
        'count_retweet': fr.fields.Integer()
    })

    @tweet_ns.expect(PostTweet)
    def post(self):
        data = flask.request.get_json()

        tw = m.Tweet.load_json(data)
        tw.save()

        return self.return_general(200, tw.__dict__)

@tweet_ns.route('/tweets')
class TweetListRoute(BaseResource):

    def get(self):
        return self.return_general(200, m.Tweet.simple_sort())

@tweet_ns.route('/tweet/keys')
class TweetKeyRoute(fr.Resource):

    def get(self, id):
        return m.db.keys()


@tweet_ns.route('/tweet/<string:id>')
class TweetIdRoute(fr.Resource):

    def get(self, id):
        return m.Tweet.get(id).__dict__

    def delete(self):
        pass

@tweet_ns.route('/retweet')
class Retweet(BaseResource):

    PostRetweet = tweet_ns.model('PostModel', {
        'user_name': fr.fields.String(),
        'title': fr.fields.String(),
        'body': fr.fields.String(),
        'retweet': fr.fields.String(),
        'count_retweet': fr.fields.Integer()
    })
    @tweet_ns.expect(PostRetweet)
    def post(self):
        data = flask.request.get_json()

        tw = m.Tweet.load_json(data)
        tw.save(write_aof=False)
        tw.increase_counter()
        m.db.bgrewriteaof()
        return self.return_general(200, tw.__dict__)

