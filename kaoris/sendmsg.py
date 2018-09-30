# coding: UTF-8
import webapp2
import json

from google.appengine.api import urlfetch

LINE_REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'


# メッセージ送信
class Massage():
    @classmethod
    def reply(self, payloads):
        header = {
            "Content-Type": "application/json",
            "Authorization": ""
        }

        result = urlfetch.fetch(url=LINE_REPLY_ENDPOINT, payload=json.dumps(payloads), method=urlfetch.POST,headers=header)
        print result.status_code

    @classmethod
    def push(self, payloads):
        header = {
            "Content-Type": "application/json",
            "Authorization": ""
        }

        result = urlfetch.fetch(url=LINE_PUSH_ENDPOINT, payload=json.dumps(payloads), method=urlfetch.POST,
                                headers=header)
