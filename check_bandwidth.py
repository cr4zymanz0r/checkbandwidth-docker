import speedtest
from datetime import datetime
import os
import os.path
import json
import mysql.connector

cfg_name = '/root/config/config.json'

try:
	with open(cfg_name) as configfile:
		config_text = configfile.read()
except:
	print(cfg_name + " not present.")
	exit(0)
	
config = json.loads(config_text)
conn_type = config['conn_type']

timenow = datetime.now()
dbhost = config['dbhost']
dbuser = config['dbuser']
dbpass = config['dbpass']
dbname = config['dbname']
dbtable = config['dbtable']
ulcolumn = config['ulcolumn']
dlcolumn = config['dlcolumn']
datecolumn = config['datecolumn']

bwtest = speedtest.Speedtest()
#bestserver = bwtest.get_best_server()
#bwtest.set_mini_server(bestserver)
dspeed = bwtest.download() / 1000000 #mbit
uspeed = bwtest.upload() / 1000000 #mbit

sqlconnection = mysql.connector.connect(user=dbuser, password=dbpass, host=dbhost, database=dbname)
cursor = sqlconnection.cursor()
add_bandwidth = ("INSERT INTO " + dbtable + " (" + dlcolumn +", " + ulcolumn + ", " + datecolumn + ") VALUES (%s, %s, %s)")
bandwidth_data = (dspeed, uspeed, timenow)
cursor.execute(add_bandwidth, bandwidth_data)

sqlconnection.commit()
sqlconnection.close()
