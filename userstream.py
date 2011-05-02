# -*- coding: utf-8 -*-
import tweepy
import settings
import urllib
import json
import pattern
from tweepy.models import Status
import random


class UserStream(tweepy.Stream):

   def user_stream(self, async=False):
        params = {'delimited': 'length'}
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        if self.running:
            raise TweepError('Stream object already connected!')
        self.url = '/2/user.json'
        self.parameters = params 
        self.body = urllib.urlencode(params)
        self.host = "userstream.twitter.com"
        self.scheme = "https://"
        self.headers['User-Agent'] = "tohae_call"
        self._start(async)
 
class UserStreamListener(tweepy.StreamListener):
    
    def on_data(self, data):
        try:
            data = json.loads(data)
            if "event" in data:
              print data["event"]
              print data

            if "event" in data and data["event"] == "favorite":
                auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
                ta = tweepy.API(auth)
                update_list = [u"何勝手にふぁぼってんの？", u"無断favorite禁止！",u"ふぁぼってくれてありがとう…（／／／）",
                    u"きらっ☆（ゝω・）v",
                    u"綺羅星",
                ] 
                ta.update_status(random.choice(update_list))
            elif "event" in data and data["event"] == "list_member_added":
                auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
                ta = tweepy.API(auth)

                ta.update_status(u"%sに颯爽登場！" % data["target_object"]["full_name"])
            elif "event" in data and data["event"] == "follow":
                auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
                ta = tweepy.API(auth)
                ta.create_friendship(screen_name = data["source"]["screen_name"])

            elif "in_reply_to_status_id" in data:
                if "event" in data:
                    pass
                else:
                    status = Status.parse(self.api, data)
                    if pattern.reply(status.text):
                        patterns = pattern.REPLIES + pattern.PATTERNS + pattern.OTHER
                    else:
                        patterns = pattern.PATTERNS

                    for p in patterns:
                        ap = p(status.text,status.user.screen_name)
                        if ap.match():
                            print ap.__class__.__name__
                            update = ap.update()
                            break
                    else:
                        update = False

                    if update and status.user.screen_name != "tohae_call" and status.user.screen_name != "fuba_recorder" and status.user.screen_name !="Korok" and status.user.screen_name != "call_juiz":
                        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
                        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
                        ta = tweepy.API(auth)
                        
                        if ap.is_reply():
                            update = "@%s %s" % ( status.user.screen_name , update)
                            ta.update_status(update,status.id)
                        else:
                            ta.update_status(update)
        except Exception, e:
            print e



if __name__ == "__main__":
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    us = UserStream(auth,UserStreamListener(),timeout = None)
    us.user_stream()
    #a.update_status("hogehoge")
    #stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

