#!/usr/bin/python3

import speedtest
from datetime import datetime
import pytz
import os
import os.path
import json
import mysql.connector
import math
import tweepy

cfg_name = '/root/config/config.json'

try:
	with open(cfg_name) as configfile:
		config_text = configfile.read()
except:
	print(cfg_name + " not present.")
	exit(0)
	
config = json.loads(config_text)

timezonetext = config['timezone']
timenow = datetime.now()
timezone = pytz.timezone(timezonetext)

tweet = config['tweet']
sql = config['sql']
tweetmegabitthreshold = config['tweetmegabitthreshold']

try:
	bwtest = speedtest.Speedtest()
	#bestserver = bwtest.get_best_server()
	#bwtest.set_mini_server(bestserver)
	dspeed = bwtest.download() / 1000000 #mbit
	uspeed = bwtest.upload() / 1000000 #mbit
except:
	print("Issue running speed test (no connectivity?)")
	exit(0)

if (dspeed and sql):
	dbhost = config['dbhost']
	dbuser = config['dbuser']
	dbpass = config['dbpass']
	dbname = config['dbname']
	dbtable = config['dbtable']
	ulcolumn = config['ulcolumn']
	dlcolumn = config['dlcolumn']
	datecolumn = config['datecolumn']

	sqlconnection = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost, database=dbname)
	cursor = sqlconnection.cursor()
	add_bandwidth = ("INSERT INTO " + dbtable + " (" + dlcolumn +", " + ulcolumn + ", " + datecolumn + ") VALUES (%s, %s, %s)")
	bandwidth_data = (dspeed, uspeed, timenow)
	cursor.execute(add_bandwidth, bandwidth_data)

	try:
		sqlconnection.commit()
		sqlconnection.close()
	except Exception as e:
		print("Problem logging to SQL: " + str(e))

if (dspeed and dspeed < tweetmegabitthreshold and tweet):
	print("attempting tweet")
	consumer_key = config['twitter_consumer_key']
	consumer_secret = config['twitter_consumer_secret']
	access_token = config['twitter_access_token']
	access_token_secret = config['twitter_access_secret']
	tweetcontents = config['tweetcontents']
	tweetcontents = tweetcontents.replace("<SPEED>", str(math.trunc(dspeed)) )
	tweetcontents = tweetcontents.replace("<DATETIME>", timenow.astimezone(timezone).strftime("%Y-%m-%d %I:%M:%S %p %Z") )
	tweetcontents = tweetcontents.replace("<TWEETTHRESHOLD>", str(tweetmegabitthreshold))

	# authentication of consumer key and secret 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	
	# authentication of access token and secret 
	auth.set_access_token(access_token, access_token_secret) 
	api = tweepy.API(auth) 
	
	# update the status (tweet)
	try:
		tweetobject = api.update_status(status = tweetcontents)
	except Exception as e:
		print("Problem Tweeting: " + str(e))
