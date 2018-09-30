# coding: UTF-8
import webapp2
import sys
import os
import json
import hmac
import hashlib

from kaoris.db import Account
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"
LINE_GET_PROFILE = "https://api.line.me/v2/bot/profile/"
LINE_CHANNEL_SECRET = ""
LINE_CHANNEL_ID = ""
LINE_CHANNEL_ACCESS_TOKEN = ""


class Message(ndb.Model):
    # NDBインスタンスの作成
    text = ndb.TextProperty()
    msgtype = ndb.StringProperty()
    sender = ndb.StringProperty(indexed=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    body = ndb.TextProperty()

    # イベントタイプの分類,NDB格納
    @classmethod
    def create(self, string):
        global message
        params = json.loads(string)
        event_type = params['type']

        # ユーザータイプ判別
        if params['source']['type'] == 'user':
            message = Message.get_or_insert(params['source']['userId'])
            message.sender = params['source']['userId']

            # イベントタイプ判別
            if event_type == 'message':
                message_type = params['message']['type']

                if message_type == 'text':
                    message.text = params['message']['text']

                    # メッセージ処理をキューに追加
                    taskqueue.add(url='/tasks/generate', params={'replytoken': params['replyToken'], 'text': message.text, 'sender': message.sender})

                if message_type == 'image':
                    pass
                if message_type == 'video':
                    pass
                if message_type == 'audio':
                    pass
                if message_type == 'location':
                    pass
                if message_type == 'sticker':
                    pass

            elif event_type == 'postback':
                pass
            elif event_type == 'follow':
                # メッセージ処理をキューに追加
                taskqueue.add(url='/tasks/generate', params={'replytoken': params['replyToken'], 'text': "@flow_event"})

            elif event_type == 'unfollow':
                pass
            elif event_type == 'join':
                pass
            elif event_type == 'leave':
                pass
            elif event_type == 'beacon':
                pass

        elif params['source']['type'] == 'group':
            pass
            # message = Message.get_or_insert(params['source']['groupId'])
            # message.sender = params['source']['groupId']

        elif params['source']['type'] == 'room':
            pass
            # message = Message.get_or_insert(params['source']['roomId'])
            # message.sender = params['source']['roomId']


        # DB書き込み

        message.msgtype = message_type
        message.body = string
        message.put()


class Signature():
    @classmethod
    def create(self, given, body, address):
        calcurated = hmac.new(LINE_CHANNEL_SECRET, body, hashlib.sha256).digest().encode('base64').rstrip()
        is_valid = False
        if given == calcurated:
            is_valid = True
        return is_valid


class ParseMessageHandler(webapp2.RequestHandler):
    def post(self):
        Message.create(self.request.get('message'))
        self.response.write('ok')


class ReceiveHandler(webapp2.RequestHandler):
    def post(self):
        given = self.request.get('signature')
        body = self.request.get('body').encode('utf8')
        address = self.request.get('address')
        events = json.loads(self.request.get('body').encode("utf-8"))['events']

        signatures = Signature.create(given, body, address)

        if signatures:
            for event in events:
                taskqueue.add(url='/tasks/parse', params={'message': json.dumps(event)})
        else:
            pass
        self.response.write('ok')


app = webapp2.WSGIApplication([
    ('/tasks/receive', ReceiveHandler),
    ('/tasks/parse', ParseMessageHandler),
], debug=True)
