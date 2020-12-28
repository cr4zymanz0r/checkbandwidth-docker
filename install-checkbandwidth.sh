#!/bin/sh

apt-get update

apt-get install python3 python3-pip -y
pip3 install speedtest-cli mysql-connector-python tweepy pytz
