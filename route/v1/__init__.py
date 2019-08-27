import os

from flask import Blueprint, url_for, current_app
from flask_restplus import Api

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if current_app.config.get('FLASK_HOST_PORT') in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


api = MyApi(api_v1, version='1.0', title='Twitter API',
            description='A simple Twitter API', )

# ns = api.namespace('kubernete', description='Kubernete operations')
__PARENT_NAMESPACE__ = 'twitter'


def init_app(app):
    """

    :param Flask app:
    :return:
    """
    from .tweet import tweet_ns
    api.add_namespace(tweet_ns)


    app.register_blueprint(api_v1)
    return app
