# -*- coding: utf-8 -*-
from app import app
from flask import url_for, request, session, jsonify, flash, redirect
from flask_oauthlib.client import OAuth

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
        session['twitter_oauth'] = resp
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
    return jsonify({"data": me.data})


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
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


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