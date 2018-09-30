# coding: UTF-8
import webapp2
import sys
import os
import json
import register
import analyze
import random

from sendmsg import Massage
from db import Account, UserTask
from datetime import datetime

from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import ndb



# 飛んできたメッセージの分類
def _check_message(reply_token, text, sender):
    userdata = Account.get_or_insert(sender)
    print userdata.flag
    print reply_token

    if text == "@flow_event":
        register.reg0(reply_token, text, userdata)
    elif text == u"予定登録":

        payloads = {

            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": u"追加する予定やお知らせを入力してください。\n（例）２月３日の１３時より、経済学の定期試験があります。資料の持ち込みは不可です。皆さん頑張りましょう！"
                },
            ]
        }

        Massage.reply(payloads)
        userdata.flag = "addtask"
        userdata.put()

    elif userdata.flag == "addtask":
        add_task(text)

    elif userdata.flag == None or userdata.flag == "false":

        payloads = {

            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": u"只今、メンテナンスモード中です。"
                },
            ]
        }

        Massage.reply(payloads)

    elif text == "@flow_event":
        register.reg0(reply_token, text, userdata)

    elif userdata.flag == "reg1":
        register.reg1(reply_token, text, userdata)

    elif userdata.flag == "reg2":
        register.reg2(reply_token, text, userdata)

    elif userdata.flag == "reg3":
        register.reg3(reply_token, text, userdata)

# workerからのからのメッセージ受け取り
class MessagingHandler(webapp2.RequestHandler):
    def post(self):
        _check_message(self.request.get('replytoken'), self.request.get('text'), self.request.get('sender'))
        self.response.write('ok')

app = webapp2.WSGIApplication([
    ('/tasks/generate', MessagingHandler),
], debug=True)
