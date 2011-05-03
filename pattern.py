# -*- coding:utf8 -*-
import re
import datetime
import random
from pyquery import PyQuery as pq
import urllib
import urllib2
import feedparser
import json
import operator
from dateutil import relativedelta
import calendar
import yaml
import tweepy
import settings

def reply(text):
    pattern = (
        u"@tohae_call",
        u"@トハエコ",
        u"@とはえコ",
        u"@とはえこ",
        u"@とはえコール",
    )
    p = re.compile("|".join(pattern))
    return p.match(text)

def keyphrase_extract(text):
    url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
    params = {
        "appid": settings.YAHOO_APPID,
        "sentence":text.encode("utf-8"),
        "output":"json",
    }
    json_data = urllib2.urlopen(url,urllib.urlencode(params)).read()
    result = json.loads(json_data)
    return result


# 必ずこれを継承する
class AbstractPattern(object):
    def __init__(self,text,posted_user=""):
        self.text = text
        self.posted_user = posted_user
        class_name =  self.__class__.__name__.lower()
        self.yaml = yaml.load(open("yaml/%s.yml" % class_name))
        if "is_reply" in self.yaml:
          self._is_reply = self.yaml["is_reply"]
        else:
          self._is_reply = False


    # tweetの中にパターンが含まれているかどうかを判定
    def _search(self,pattern):
        if isinstance(pattern,list):
          pattern = "|".join(pattern)

        p = re.compile(pattern)
        return p.search(self.text)

    # 発言候補のリストの中からランダムにひとつ取得
    def _random(self,kouho):
        return random.choice(kouho)

    def is_reply(self):
        return self._is_reply

    def match(self):
        return self._search(self.yaml["pattern"])

    def update(self):
        kouho = self.yaml["kouho"]
        return self._random(kouho)


class CronPattern(AbstractPattern):
    def __init__(self):
        self.today = datetime.datetime.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.hour = self.today.hour
        self.minute = self.today.minute

class Nandeinaino(AbstractPattern):
    def update(self):
        today = datetime.datetime.today()
        hour = today.hour
        weekday = today.weekday()
        client = self.client
        
        if 2 < hour < 9:
            text = u"とはえなら俺の横で寝てるよ"

        elif weekday < 5 and 10 < hour < 19 :
            text = u"とはえは仕事してるんじゃないですかね？"

        elif client == "twicca":
            text = u"とはえはたぶん外出してるよ！"

        elif client == "YoruFukurou" or client == "Twitter for iPad":
            text = u"とはえは引きこもってると思います！呼び出せばきっと来てくれるよ！"
        else:
            text = u"知るかあほ"

        return text

    def is_reply(self):
        if random.randint(0,1) == 1:
            self._is_reply = True
        return self._is_reply

    def client(self):
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
        ta = tweepy.API(auth)
        return ta.user_timeline(screen_name = "tohae")[0].source
        

class Zawa(AbstractPattern): pass

class Tohaesan(AbstractPattern): pass

class Love(AbstractPattern): pass

class Kirai(AbstractPattern): pass

class Shinitai(AbstractPattern): pass

class Elshaddai(AbstractPattern): pass

class Sayurisan(AbstractPattern): pass

class Aisatsu(AbstractPattern): pass

class Help(AbstractPattern): pass

class Yamada(AbstractPattern): pass

class Douitasimasite(AbstractPattern): pass

class Pizza(AbstractPattern): pass

class Syazai(AbstractPattern): pass

class Hagemasite(AbstractPattern): pass

class Tanoshingo(AbstractPattern): pass

class Other(AbstractPattern):
    def match(self):
        return True
    
      
#class Food(AbstractPattern):
#    def __init__(self,text,posted_user=""):
#        AbstractPattern.__init__(self,text)
#        self.text = " ".join(re.split(u" |　",text)[1:])
#
#    def match(self):
#        pattern = (
#            u"(.+)食べた",
#            u"(.+)食った",
#            u"(.+)食いたい",
#            u"(.+)飲んだ",
#            u"(.+)飲みたい",
#            u"(.+)食べる",
#        )
#        return self._search(pattern)
#
#    def update(self):
#        url = "http://makimoto.tsuyabu.in/kcal/api.py?"
#        pattern = re.compile(u"(.+)(?:食べた|食った|食いたい|飲んだ|飲みたい)")
#        m = pattern.search(self.text)
#        if m:
#            query = m.group(1)
#            params = {
#                "food": query,
#                "appid":"tohae_call",
#            }
#            json_data = urllib2.urlopen(url+urllib.urlencode(params)).read()
#            result = json.loads(json_data)
#            if random.randint(0,9) >8 or not result:
#                kouho = (
#                    u"太りますよ",
#                    u"痩せろ",
#                    u"それうまいよね",
#                    u"別腹！別腹！",
#                    u"おれにも食わせろ",
#                    u"僕はラーメンを食べます",
#                    u"僕はトマトが嫌いです",
#                )
#                update = self._random(kouho)
#            else:
#                cal = result["median"]
#                update = u"%sは%skcalです。" % (query,cal)
#        else:
#            update = u"太るぞ"
#        return update
#
#    def is_reply(self):
#        self._is_reply = True
#        return self._is_reply

class Nyaa(AbstractPattern):
    def is_reply(self):
        if random.randint(0,1) == 1:
            self._is_reply = True
        return self._is_reply


class Findjob(AbstractPattern):
    def update(self):
        url = "http://www.find-job.net/fj/newjob_rss.pl?new=1&mikeiken=1&ky_kind=year&ky_from=4200000&kinmuchi=1"
        d = feedparser.parse(url)
        if d.entries:
            entry = self._random(d.entries)
            title = entry.title
            link = entry.link
            return u"こことかどうですか？「%s」 %s" % ( title, link)

        else:
            return u"採用を募集している会社はありません。強く生きて！"

class Kensaku(AbstractPattern):
    def update(self):
        pattern = re.compile(u"(.+)って(?:何|なに|？|\?)")
        self.text = " ".join(re.split(u" |　", self.text)[1:])
        m = pattern.match(self.text)
        if m:
            query = m.group(1).encode("utf8")
            url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%3D'http%3A%2F%2Fsearch.yahooapis.jp%2FPremiumWebSearchService%2FV1%2FwebSearch%3Fappid%3DX1gsNiixg67PNs4qxlYkfL2Z.Ckmu_M3ejFdHG4VbuaLc1DpYAix7MwkcP8PAkRb%26results%3D1%26query%3D" + urllib.quote_plus(query) + "'&format=json&diagnostics=true&callback=" 
            json_data = urllib2.urlopen(url).read()
            result = json.loads(json_data)
            title = result["query"]["results"]["ResultSet"]["Result"]["Title"]
            link = result["query"]["results"]["ResultSet"]["Result"]["Url"]
            update = u"ご参考「%s」 %s" % ( title, link)

        else:
            update = u"ぐぐれかす"

        return update
    
class PupeRemind(CronPattern):
    def match(self):
        return self.hour == 23 and 54 <= self.minute < 56

    def update(self):
        if self.day == calendar.monthrange(self.year,self.month)[1]:
            return u"今月は皆勤賞を取れましたか？取れた人はおめでとうございます。取れなかった人は来月こそはがんばってください"
        return u"プーペガールの着せ替えはすませましたか？皆勤賞目指してがんばってください！"



class Oshiete(AbstractPattern):
    def update(self):
        text = " ".join(re.split(u" |　",self.text)[1:])
        text = text.split(u"教えて")[0]
        url = "http://oshiete.goo.ne.jp/search_goo/result/?"
        params = {
            "MT":text.encode("euc-jp"),
            "mt_opt":"a",
            "qatype":"qa",
            "st":"all",
            "sr":"norm",
            "tf":"all",
            "good":"0",
            "dc":"10",
            "type":"rss",
        }
        goo_url = url + urllib.urlencode(params)
        d = feedparser.parse(goo_url)
        if d.entries:
            title = d.entries[0].title
            link = d.entries[0].link
        else:
            phrase = keyphrase_extract(text)
            if phrase:
                sorted_list = sorted(phrase.items(),key=operator.itemgetter(1),reverse=True)
                params["MT"] = " ".join([ a[0] for a in sorted_list[0:1]]).encode("euc-jp")
                goo_url = url + urllib.urlencode(params)
                print goo_url
                d = feedparser.parse(goo_url)
                if d.entries:
                    title = d.entries[0].title
                    link = d.entries[0].link
        
        #TODO Bug
        if title:
            return u"教えてあげる！「%s」 %s" % (title,link)
        else:
            return u"ごめん、ぼくにはわからないや…"


class Unsei(AbstractPattern):
    def match(self):
        self.pattern = [
            u"牡羊座",u"おひつじ座",
            u"牡牛座",u"おうし座",
            u"双子座",u"ふたご座",
            u"蟹座",u"かに座",
            u"獅子座",u"しし座",
            u"乙女座",u"おとめ座",
            u"天秤座",u"てんびん座",
            u"蠍座",u"さそり座",
            u"射手座",u"いて座",
            u"山羊座",u"やぎ座",
            u"水瓶座",u"みずがめ座",
            u"魚座",u"うお座",
        ]
        if self._search(self.pattern):
            return self._search(u"運勢")
        else:
            return None

    def update(self):
        #uranai_url = "http://fortune.yahoo.co.jp/12astro/%04d%02d%02d/%s.html"
        uranai_url = "http://uranai.nifty.com/app/cs/f12seiza/detail/%04d%02d%02d-%d/1.htm"
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        day = today.day
        if u"明日" in self.text:
            tommorow = today + relativedelta.relativedelta(days=+1)
            year = tommorow.year
            month = tommorow.month
            day = tommorow.day

        for seiza in self.pattern:
            if self._search(seiza):
                if seiza == u"牡羊座" or seiza == u"おひつじ座":
                    constellation = 1
                elif seiza == u"牡牛座" or seiza == u"おうし座":
                    constellation = 2
                elif seiza == u"双子座" or seiza == u"ふたご座":
                    constellation = 3
                elif seiza == u"蟹座" or seiza == u"かに座":
                    constellation = 4
                elif seiza == u"獅子座" or seiza == u"しし座":
                    constellation = 5
                elif seiza == u"乙女座" or seiza == u"おとめ座":
                    constellation = 6
                elif seiza == u"天秤座" or seiza == u"てんびん座":
                    constellation = 7
                elif seiza == u"蠍座" or seiza == u"さそり座":
                    constellation = 8 
                elif seiza == u"射手座" or seiza == u"いて座":
                    constellation = 9
                elif seiza == u"山羊座" or seiza == u"やぎ座":
                    constellation = 10
                elif seiza == u"水瓶座" or seiza == u"みずがめ座":
                    constellation = 11
                elif seiza == u"魚座" or seiza == u"うお座":
                    constellation = 12

                uranai_url = uranai_url % (year,month,day,constellation)

                print uranai_url
                d = pq(uranai_url)
                point = d(".hako").html()
                midashi = d(".pad_5 p").html().split(u"。")[0]
                rennaiun = d(".right p:eq(0)").html()
                lucky_color = d(".hako2 p").html()
                lucky_item = d(".hako4 p").html()

                pixiv = {"key" : settings.PIXIV_APPID}
                pixiv_api = "http://p.tl/api/api_simple.php?"
                pixiv["url"] = uranai_url
                json_data = urllib2.urlopen(pixiv_api + urllib.urlencode(pixiv)).read()
                result = json.loads(json_data)
                uranai_url = result["short_url"]
                return u"総合運は%s、%s。%s%sの%sを持つと良いでしょう。 %s" % ( point,midashi,rennaiun,lucky_color,lucky_item,uranai_url)
                
class Pantsu(AbstractPattern):
    def update(self):
        favotter_url = "http://favotter.matope.com/user/tohae"
        try:
            d = pq(url=favotter_url)
            lv = d(".bubble:eq(0)").attr("class").strip().split(" ")[-1]
            if lv == "LV1":
                return u"黒だよ！"
            elif lv == "LV2":
                return u"ミドリだよ☆"
            elif lv == "LV3" or lv == "LV4":
                return u"今日はむらさきなのー"
            elif lv == "LV5" or lv == "LV6":
                return u"勝負の赤色！！"
            else:
                return u"そんなの恥ずかしくて言えないよー＞＜"        
        except Exception, e:
            return u"ぱんちゅサーバが落ちてるみたい"        
            

class Harahe(AbstractPattern):
    def update(self):
        url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?"
        params = {
            "key":"3c3f8a139b88774f",    
            "count":"20",
            "order":"4",
            "format":"json",
            "type":"lite",
        }
        phrase = keyphrase_extract("".join(re.split(u" |　",self.text)[1:]))
        if phrase:
            sorted_list = sorted(phrase.items(),key=operator.itemgetter(1),reverse=True)
            params["keyword"] = " ".join([ a[0] for a in sorted_list[0:2]]).encode("utf-8")
        else:
            params["small_area"] = "X130"
        
        json_data = urllib2.urlopen(url+urllib.urlencode(params)).read()
        result = json.loads(json_data)
        if result["results"]["shop"]:
            return self._get_shop(result)
        else:
            params.pop("keyword")
            params["small_area"] = "X130"
            json_data = urllib2.urlopen(url+urllib.urlencode(params)).read()
            result = json.loads(json_data)
            return self._get_shop(result)

    def _get_shop(self,result):
        index = random.randint(0,len(result["results"]["shop"]) - 1) 
        shop = result["results"]["shop"][index] 
        shop_name =shop["name"]
        shop_url = shop["urls"]["pc"]
        shop_catch = shop["genre"]["catch"]
        return u"とはえを誘って、「%s 『%s』」に行けば良いと思うよ！ %s" % (shop_catch, shop_name, shop_url)
    



#TODO 中日戦の結果
class Baseball(AbstractPattern):
    def match(self):
        self.pattern =(
            u"阪神",u"タイガース",
            u"中日",u"ドラゴンズ",
            u"巨人",u"ジャイアンツ",
            u"ヤクルト",u"スワローズ",
            u"横浜",u"ベイスターズ",
            u"広島",u"カープ",
            u"日ハム",u"ファイターズ",
            u"ソフトバンク",u"ホークス",
            u"ロッテ",u"マリーンズ",
            u"西武",u"ライオンズ",
            u"楽天",u"ゴールデンイーグルス",
            u"オリックス",
        )
        return self._search(self.pattern)

    def update(self):
        team = ""
        for p in self.pattern:
            if self._search((p,)):
                if p == u"阪神" or p == u"タイガース":
                    team = "Tigers_Flash"
                elif p == u"中日" or p == u"ドラゴンズ":
                    team = "DRAGONS_Flash"
                elif p == u"巨人" or p== u"ジャイアンツ":
                    team = "GIANTS_Flash"
                elif p == u"ヤクルト" or p== u"スワローズ":
                    team = "Swallows_Flash"
                elif p == u"横浜" or p== u"ベイスターズ":
                    team = "BayStars_Flash"
                elif p == u"広島" or p== u"カープ":
                    team = "Carp_Flash"
                elif p == u"日ハム" or p== u"ファイターズ":
                    team = "FIGHTERS_Flash"
                elif p == u"ソフトバンク" or p== u"ホークス":
                    team = "HAWKS_Flash"
                elif p == u"ロッテ" or p== u"マリーンズ":
                    team = "Marines_Flash"
                elif p == u"西武" or p== u"ライオンズ":
                    team = "Lions_Flash"
                elif p == u"楽天" or p== u"ゴールデンイーグルス":
                    team = "EAGLES_Flash"
                elif p == u"オリックス":
                    team = "Buffaloes_Flash"
                
                url = "http://twitter.com/statuses/user_timeline/%s.rss" % team
                g = feedparser.parse(url)
                return "".join(g.entries[0].summary_detail.value.split(" ")[3:])
                
                

    def is_reply(self):
        self._is_reply = True
        return self._is_reply


class Eco(CronPattern):
    def match(self):
        return self.hour == 15 and self.minute == 11

    def update(self):
        url = "http://eco.nikkeibp.co.jp/rss/eco/eco.rdf"
        d = feedparser.parse(url)
        title = d.entries[0].title
        link = d.entries[0].link
        category = d.entries[0].tags[0]["term"].split("_")[1]
        return u"とはえこニュース:【%s】%s %s" % ( category,title,link)


class Birthday(CronPattern):
    def match(self):
        birthday_list = [
            (1,1,"とはえ甥",),
            (1,5,"mirakui",),
            (1,10,"riafel",),
            (1,18,"t_meitei",),
            (3,9,"yokochie",),
            (3,18,"fykr",),
            (4,18,"magic_holic",),
            (5,12,"Azmin",),
            (5,12,"Azmin",),
            (5,20,"plus7minus11",),
            (8,1,"haseryo",),
            (9,15,"navigatoria",),
            (10,29,"ono_matope",),
            (11,18,"wolf_robin",),
            (10,15,"makimoto",),
            (12,19,"haseryo",),
        ]

        if self.hour == 0 and 0 <= self.minute <2:
            for month,day,user in birthday_list:
                if self._check(month,day):
                    self.dear = user
                    return True
        else:
            return False
        return True

    def _check(month,day):
        return self.today.month == month and self.today.day == day

    def update(self):
        return "@%s 誕生日おめでとうございます！！！！！！！" % self.dear

class FubaRecorder(AbstractPattern):
    def update(self):
        text = " ".join(re.split(u" |　",self.text)[1:])
        return u"@フバレコ " + text
    
    #TODO fuba_recorderからの返事をRT
    def rt(self):
        pass

        
#TODO ろうひ君を移植
class Rouhikun(AbstractPattern):
    def match(self):
        pattern =(
            u"[\d]+円",
        )
        return self._search(pattern)

    def update(self):
        hdb = pytc.HDB()
        try:
            hdb.open("/home/tohae/codetsuyabu/repos/tohae/bot/rouhi.tch",pytc.HDBOWRITER | pytc.HDBOCREAT)
            #hdb.addint(self.posted_user,
            
        except pytc.Error,(ecode,errmsg):
            print errmsg
        finally:
            hdb.close    
        return self._random(kouho)

    def is_reply(self):
        self._is_reply = True
        return self._is_reply




class Weather(AbstractPattern):
    def update(self):
        """
        0-12時は今日の天気
        12-24時は明日の天気
        """
        today = datetime.datetime.today()
        tokyo = "http://rss.weather.yahoo.co.jp/rss/days/4410.xml"
        d = feedparser.parse(tokyo)
        if 12 < today.hour < 24:
            tommorow = today + relativedelta.relativedelta(days=+1)
            day = tommorow.day
        else:
            day = today.day

        p = re.compile(u"【 %d日*" % day)
        for i,e in enumerate(d.entries):
            if p.match(e.title):
                sd = e.title.split(" ")
                update = u"%sの%sの天気は%s、最高気温%s、最低気温%sです。" % ( sd[1], sd[2].split(" (")[0], sd[4], sd[6].split("/")[0], sd[6].split("/")[1] )

                break

        return update


class Translation(AbstractPattern):
    def match(self):
        japanese = re.compile(u"[あ-んア-ン]+")
        self.text = " ".join(re.split(u" |　",self.text)[1:])
        return None == japanese.search(self.text)

    def update(self):
        url = "http://pipes.yahoo.com/poolmmjp/ej_translation_api?"
        params = {
            "_render":"rss",
            "text":self.text
        }
        request_url = url + urllib.urlencode(params)
        print request_url.replace(r"+","%20")
        d = feedparser.parse(request_url.replace(r"+","%20"))
        return u"こういう意味？「%s」" % d.entries[0].summary

    def is_reply(self):
        self._is_reply = True
        return self._is_reply

class Len(AbstractPattern):
    def match(self):
        return len(self.text) > 80

class Tsuitou(AbstractPattern):
    def update(self):
        return self.posted_user + u"追悼…"



class Echo(AbstractPattern):
    def update(self):
        self.text = " ".join(re.split(u" |　",self.text)[1:])
        return self.text.split(u"って言え")[0]

class Tiqav(AbstractPattern):
    def update(self):
        pattern = re.compile(r"(http://tiqav.com/([\w\d]+))")
        m = pattern.search(self.text)
        if m:
            query = m.group(0)
            d = pq(query)
            return "http://tiqav.com" + d(".mini_content_hover a").attr("href")
        else:
            return "http://tiqav.com" + d(".box a").attr("href")



PATTERNS =(
    Echo,
    Nandeinaino,
    Zawa,
    Tohaesan,
    #Sayurisan,
    Findjob,
    Nyaa,
    Shinitai,
    Yamada,
    Tsuitou,
)

REPLIES =(
    Pizza,
    Len,
    Kensaku,
    Love,
    Kirai,
    Unsei,
    Weather,
    Harahe,
#    Food,
    Oshiete,
    FubaRecorder,
    Pantsu,
    Aisatsu,
    Help,
    Douitasimasite,
    Elshaddai,
    Syazai,
    Tiqav,
    Hagemasite,
    Tanoshingo,
    #Translation,
)

OTHER = (
    Other,
)

CRON =(
    Eco,
    PupeRemind,
    Birthday,
)

