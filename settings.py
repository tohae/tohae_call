# -*- coding: utf-8 -*-
#Your Application's Consumer Key and Secret                      
from pit import Pit
config = Pit.get("tohae_call")
CONSUMER_KEY = config["CONSUMER_KEY"]
CONSUMER_SECRET = config["CONSUMER_SECRET"]
ACCESS_TOKEN = config["ACCESS_TOKEN"]
ACCESS_SECRET = config["ACCESS_SECRET"]

APP_NAME = u"とはえこ！！"

YAHOO_APPID = config["yahoo_appid"]
PIXIV_APPID = config["pixiv_appid"]
