# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash
from flask_peewee.utils import get_object_or_404, object_list

from app import app
from auth import auth
from models import User


@app.route('/')
def index():
    return render_template("index.html")