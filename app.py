# -*- coding: utf-8 -*-
from flask import Flask

from flask_peewee.db import Database


app = Flask(__name__)
app.config.from_object('config.ConfigurationSqlite')

db = Database(app)

