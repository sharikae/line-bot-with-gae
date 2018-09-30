# coding: UTF-8
import json
import analyze
from sendmsg import Massage

def reg0(reply_token, text, userdata):
    payloads = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": u"登録ありがとうございます"
            },
            {
                "type": "text",
                "text": u"学校名、学部学科を教えてください\n（例）東京大学、文学部、教育学科"
            },

        ]
    }

    Massage.reply(payloads)
    userdata.flag = "reg2"
    userdata.put()

def reg01(reply_token, text, userdata):
    payloads = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": u"学校名、学部学科を教えてください\n（例）東京大学、文学部、教育学科"
            },
        ]
    }

    Massage.reply(payloads)
    userdata.flag = "reg2"
    userdata.put()


def reg2(reply_token, text, userdata):
    global org_name, und_name, dep_name
    org_name = u"見つかりません"
    und_name = u"見つかりません"
    dep_name = u"見つかりません"

    rip1 = text.replace(" ", u"、")
    rip2 = rip1.replace(u"　", u"、")
    rip3 = u"私はねー！、" + rip2 + u"なんだよー。"
    print "TEXT_STRIP"
    print rip3.encode('utf8')
    print "TEXT_STRIP"

    result = analyze.analyze_entities(rip3, analyze.get_native_encoding_type())
    entities = json.dumps(result.values())
    print type(entities)
    print type(result)
    print(result.keys())
    print(result.values())
    print(result.items())

    for entitie in result['entities']:
        print "====="
        print entitie['type']
        print entitie['name'].encode('utf8')
        print "====="
        if entitie['type'] == "ORGANIZATION" and u"大学" in entitie['name']:
            org_name = entitie['name']
        for mention in entitie['mentions']:
            if entitie['type'] == "ORGANIZATION" and mention['type'] == "COMMON":
                print "====="
                print "GAKUBU"
                print mention['text']['content'].encode('utf8')
                print "======"
                und_name = mention['text']['content']
            elif entitie['type'] == "OTHER":
                print "====="
                print "GAKKA"
                print mention['text']['content'].encode('utf8')
                print "======"
                dep_name = mention['text']['content']
            print "ALL_MENTIONS"
            print mention['type'].encode('utf8')
            print mention['text']['content'].encode('utf8')
            print "ALL_MENTIONS"

    parse = u"学校名: " + org_name + u"\n学部名: " + und_name + u"\n学科名: " + dep_name + u"\nよろしいですか？"

    payloads = {

        "replyToken": reply_token,
        "messages": [
            {
                "type": "template",
                "altText": parse,
                "template": {
                    "type": "confirm",
                    "text": parse,
                    "actions": [
                        {
                            "type": "message",
                            "label": u"はい",
                            "text": u"はい"
                        },
                        {
                            "type": "message",
                            "label": u"修正",
                            "text": u"修正"
                        }
                    ]
                }
            }
        ]
    }

    Massage.reply(payloads)

    userdata.flag = "reg3"

    if org_name != u"見つかりません":
        userdata.school = org_name
    if und_name != u"見つかりません":
        userdata.undergraduate = und_name
    if dep_name != u"見つかりません":
        userdata.department = dep_name

    userdata.put()


def reg3(reply_token, text, userdata):
    if text == u"はい":

        payloads = {

            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": u"登録完了です！\nさっそく予定を登録しましょう。\n詳しい使い方は↓のメニューよりご覧いただけます。"
                }
            ]
        }

        Massage.reply(payloads)
        userdata.flag = "false"
        userdata.put()

    else:
        reg01(reply_token, text, userdata)