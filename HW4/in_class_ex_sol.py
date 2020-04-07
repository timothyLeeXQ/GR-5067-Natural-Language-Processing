# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:46:31 2017

@author: pathouli
"""
import tweepy
from textwrap import TextWrapper
from twitter_sniffer_sol import sniffer

#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

#the_regex = '#motivation,#positivity,#happy,#positivevibes,#life,#inspiration,#positivity,#success'
the_regex = 'pelosi'

auth = tweepy.auth.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')

myStreamListener = sniffer()

#Get trained model
#tfidf, pca, model = model_train()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=[the_regex])