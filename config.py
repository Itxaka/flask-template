# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = ''


class Configuration(object):
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = DEBUG
    SECRET_KEY = SECRET_KEY


class ConfigurationMysql(object):
    DATABASE = {
        'name': '',
        'engine': 'peewee.MySQLDatabase',
        'host': '',
        'user': '',
        'passwd': '',
    }
    DEBUG = DEBUG
    SECRET_KEY = SECRET_KEY