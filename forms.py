# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo


class RegisterForm(Form):
    username = TextField(validators=[InputRequired])
    password = PasswordField(validators=[InputRequired(), EqualTo("confirm", message="Passwords don't match")])
    confirm = PasswordField()
    email = TextField(validators=[Email])
