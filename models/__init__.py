# coding=utf-8
import redis
import rom

from app import app

DB_IP = app.config.get('DATABASE_IP', '127.0.0.1')
DB_PORT = app.config.get('DATABASE_PORT', 6379)
db = redis.Redis(
        host=DB_IP,
        port=DB_PORT
)

def init_app(app, **kwargs):


    print('Start app with database: %s:%s' %
          (DB_IP, DB_PORT))
    return app



class JSONParsedProperty(object):
    """ Biểu diễn 1 thuộc tính dựa trên việc parse 1 thuộc tính khác của object
    theo JSON
    """

    def __init__(self, raw_property_name):
        """
        :param str raw_property_name: tên của thuộc tính chứa thông tin raw
        """
        self.raw_property_name = raw_property_name
        self.parsed_property_name = '_parsed_%s_' % raw_property_name

    def __get__(self, instance, owner):
        # Trả về giá trị của property nếu gọi = class
        if instance is None:
            return self

        # Nếu giá trị raw bị thay đổi sau khi gọi giá trị JSON, giá trị JSON
        # sẽ không được update lại theo giá trị mới
        try:
            return instance.__getattribute__(self.parsed_property_name)
        except AttributeError:  # this property has not been parsed
            # parse property's value
            raw_val = instance.__getattribute__(self.raw_property_name)
            if raw_val:
                parsed_value = utils.json_decode(raw_val)
            else:
                parsed_value = None

            # set the parsed value, mark property parsed
            setattr(instance, self.parsed_property_name, parsed_value)
            return parsed_value

    def __set__(self, instance, value):
        setattr(instance, self.parsed_property_name, value)
        setattr(instance, self.raw_property_name, utils.json_encode(value))


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()
#
#
# # @app.after_request
# def shutdown_session(response):
#     db.session.commit()
#     db.session.remove()
#     return response


from .tweet import *
from .user import *
