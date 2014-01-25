# -*- coding: utf-8 -*-


class Configuration(object):
    DEBUG = True
    SECRET_KEY = ""
    GOOGLE_ID = ""
    GOOGLE_SECRET = ""
    FACEBOOK_APP_ID = ""
    FACEBOOK_APP_SECRET = ""
    TWITTER_KEY = ""
    TWITTER_SECRET = ""

class ConfigurationSqlite(Configuration):
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }


class ConfigurationMysql(Configuration):
    DATABASE = {
        'name': '',
        'engine': 'peewee.MySQLDatabase',
        'host': '',
        'user': '',
        'passwd': '',
    }