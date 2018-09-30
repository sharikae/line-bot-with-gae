# coding: UTF-8
from google.appengine.ext import ndb


class Account(ndb.Model):
    userid = ndb.StringProperty()       # ユーザーID,KEY LINEのユーザーIDと同一
    username = ndb.StringProperty()     # LINE 表示名
    pictureurl = ndb.StringProperty()   # LINE アイコンURL
    userstatus = ndb.StringProperty()   # LINE ひとこと
    character = ndb.StringProperty()    # BOT の性格
    studentid = ndb.StringProperty()    # 学籍番号
    schoolyear = ndb.StringProperty()   # 学年
    school = ndb.StringProperty()       # 学校名
    department = ndb.StringProperty()   # 学科
    undergraduate = ndb.StringProperty()# 学部
    setupflag = ndb.BooleanProperty()   # 特殊操作時フラグ
    flag = ndb.StringProperty()         # アカウント作成日時
    date = ndb.DateTimeProperty(auto_now_add=True)

class UserTask(ndb.Model):
    adduser = ndb.StringProperty()          # イベンtpを追加したユーザ
    eventname = ndb.StringProperty()        # タスク名
    tag_school = ndb.StringProperty()       # 対照の学校名
    tag_undergraduate = ndb.StringProperty()# 対照の学部名
    tag_department = ndb.StringProperty()   # 対照の学科名
    tag_date = ndb.DateTimeProperty()       # イベント開始時刻
    adddate = ndb.DateTimeProperty(auto_now_add=True)
