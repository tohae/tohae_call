# -*- coding:utf8 -*-
from tweepy import models
import settings
import re
import urllib
import urllib2
import json

class Status(models.Status):
    def is_reply(self):
        """tohae_call宛のメッセージかどうかを判定"""
        pattern = (
            u"@tohae_call",
            u"@トハエコ",
            u"@とはえコ",
            u"@とはえこ",
            u"@とはえコール",
        )
        p = re.compile("|".join(pattern))
        return p.match(self.text)

    def extract_keyphrase(self):
        """status.textの中からキーフレーズを抽出"""
        url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
        text = " ".join(re.split(u" |　",self.text)[1:])
        params = {
            "appid": settings.YAHOO_APPID,
            "sentence": text.encode("utf-8"),
            "output":"json",
        }
        json_data = urllib2.urlopen(url,urllib.urlencode(params)).read()
        result = json.loads(json_data)
        return result
 
