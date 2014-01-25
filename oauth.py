# -*- coding: utf-8 -*-
from app import app
from flask import url_for, request, session, jsonify, flash, redirect
from flask_oauthlib.client import OAuth
from models import User
from auth import auth

oauth = OAuth(app)

google = oauth.remote_app('google', consumer_key=app.config.get('GOOGLE_ID'),
                          consumer_secret=app.config.get('GOOGLE_SECRET'),
                          request_token_params={
                              'scope': ['https://www.googleapis.com/auth/userinfo.email',
                                        'https://www.googleapis.com/auth/userinfo.profile']
                          }, base_url='https://www.googleapis.com/oauth2/v1/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          authorize_url='https://accounts.google.com/o/oauth2/auth', )

twitter = oauth.remote_app('twitter', consumer_key=app.config['TWITTER_KEY'],
                           consumer_secret=app.config['TWITTER_SECRET'],
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',)

facebook = oauth.remote_app('facebook', consumer_key=app.config['FACEBOOK_APP_ID'],
                            consumer_secret=app.config['FACEBOOK_APP_SECRET'],
                            request_token_params={'scope': 'email'},
                            base_url='https://graph.facebook.com',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth')

@app.route('/login/twitter')
def logintwitter():
    return twitter.authorize(callback=url_for('authorizedtwitter', _external=True))


@app.route('/login/twitter/authorized')
@twitter.authorized_handler
def authorizedtwitter(resp):
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['user'] = resp['screen_name']
        print resp
        try:
            a = User.create(username=resp['screen_name'], password=resp['oauth_token_secret'])
            a.save()
        except:
            pass
        a = User.select().where(User.username == resp['screen_name']).first()
        auth.login_user(a)
    return redirect(url_for('index'))


@app.route('/login/google')
def logingoogle():
    return google.authorize(callback=url_for('authorizedgoogle', _external=True))


@app.route('/login/google/authorized')
@google.authorized_handler
def authorizedgoogle(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    session['user'] = me.data['name']
    try:
        a = User.create(username=me.data['name'], password=resp['access_token'])
        a.save()
    except:
        pass
    a = User.select().where(User.username == me.data['name']).first()
    auth.login_user(a)
    return redirect(url_for("index"))


@app.route('/login/facebook')
def loginfacebook():
    return facebook.authorize(callback=url_for('authorizedfacebook', _external=True))


@app.route('/login/facebook/authorized')
@facebook.authorized_handler
def authorizedfacebook(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    me = facebook.get('/me')
    session['user'] = me.data['name']
    print resp
    try:
        a = User.create(username=me.data['name'], password=resp['access_token'])
        a.save()
    except:
        pass
    a = User.select().where(User.username == me.data['name']).first()
    auth.login_user(a)
    return redirect(url_for("index"))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for("index"))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')