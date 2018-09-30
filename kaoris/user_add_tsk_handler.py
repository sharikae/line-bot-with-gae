# coding: UTF-8
import json
import analyze
from sendmsg import Massage

# Goo 日付正規化APIで時刻情報取り出し/正規化
def pars_datetime(text):

    header = {
        "Content-Type": "application/json",
    }

    payloads = {

        "app_id": "",
        "sentence": text
    }

    result = ult

def add_task(text):
    global eve_name # イベント名
    # usertask = analyze.get_or_insert('task1')
    result = analyze.analyze_entities(text, analyze.get_native_encoding_type())
    datetimes = pars_datetime(text)

    entities = json.dumps(result.values())

    # メタ情報表示
    print "ADD_TASK_META++++++++"
    print type(entities)
    print type(result)
    print(result.keys())
    print(result.values())
    print(result.items())
    print "ADD_TASK_META++++++++"

    for entitie in result['entities']:

        # エンティティタイプ表示
        print "ENTITE_TYPE+++++++"
        print entitie['type']
        print entitie['name'].encode('utf8')
        print "ENTITE_TYPE+++++++"
        if entitie['type'] == "EVENT":
            eve_name = entitie['name']
        for mention in entitie['mentions']:

            # その他の固有表現表示
            print "ALL_MENTIONS+++++++"
            print mention['type'].encode('utf8')
            print mention['text']['content'].encode('utf8')
            print "ALL_MENTIONS+++++++"

    date = json.loads(datetime.content)rlfetch.fetch(url='https://labs.goo.ne.jp/api/chrono', payload=json.dumps(payloads), method=urlfetch.POST, headers=header)
    return resu

    for dt in  date['datetime_list']:
        print dt[1]
        print type(dt[1])
        print type(str(dt[1]))

        # usertask.tag_date = dtime

    t = datetime.strptime('2014/01/01', '%Y/%m/%d')
    print t