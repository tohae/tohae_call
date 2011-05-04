# -*- coding:utf8 -*-
from pattern import AbstractPattern

class CronPattern(AbstractPattern):
    def __init__(self):
        self.today = datetime.datetime.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.hour = self.today.hour
        self.minute = self.today.minute

class PupeRemind(CronPattern):
    def match(self):
        return self.hour == 23 and 54 <= self.minute < 56

    def update(self):
        if self.day == calendar.monthrange(self.year,self.month)[1]:
            return u"今月は皆勤賞を取れましたか？取れた人はおめでとうございます。取れなかった人は来月こそはがんばってください"
        return u"プーペガールの着せ替えはすませましたか？皆勤賞目指してがんばってください！"

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

    def _check(self,month,day):
        return self.today.month == month and self.today.day == day

    def update(self):
        return "@%s 誕生日おめでとうございます！！！！！！！" % self.dear

CRON = CronPattern.__subclasses__()
