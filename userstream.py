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

            auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
            auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
            ta = tweepy.API(auth)
            if "event" in data:
                if data["event"] == "favorite":
                    update_list = [
                        u"きらっ☆（ゝω・）v",
                        u"綺羅星",
                        u"あっ、流れ星",
                        u"favoriteいただきましたー",
                        u"tweetする者にとってfavoriteは寿命！",
                        u"こんなものに星をつけるなんて、訳がわからないよ",
                        u"favは命より重い・・・！",
                    ] 
                    ta.update_status(random.choice(update_list))
                elif data["event"] == "list_member_added":
                    ta.update_status(u"%sに颯爽登場！" % data["target_object"]["full_name"])
                elif data["event"] == "follow":
                    ta.create_friendship(screen_name = data["source"]["screen_name"])

            elif "in_reply_to_status_id" in data:
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

                # update文字が空でなく、相手がNGユーザーでない場合
                if self.is_update(update, status.user.screen_name):
                                  
                    # リプライするパターンであれば、@とin_reply_to_status_idをつける
                    if ap.is_reply():
                        update = "@%s %s" % ( status.user.screen_name , update)
                        ta.update_status(update,status.id)
                    else:
                        ta.update_status(update)
            
            # cron
            for p in pattern.CRON:
                ap = p()
                if ap.match():
                    ta.update_status(ap.update())

        except Exception, e:
            print e

    def is_update(self, update, screen_name):
        ng_users = [
          "tohae_call",
          "fuba_recorder",
          "Korok",
          "call_juiz",
        ]

        if not update or screen_name in ng_users:
            return False
        else:
            return True



if __name__ == "__main__":
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    us = UserStream(auth,UserStreamListener(),timeout = None)
    us.user_stream()

