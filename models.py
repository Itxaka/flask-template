# -*- coding: utf-8 -*-
from flask_peewee.auth import BaseUser
from peewee import *

from app import db


class User(db.Model, BaseUser):
    username = CharField(unique=True)
    password = CharField(null=True)
    email = CharField(null=True)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)
    logged_in = BooleanField(default=False)

    def __unicode__(self):
        return self.username


User.create_table(fail_silently=True)