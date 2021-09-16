import libraryUtils
from threading import Thread, Timer
import json
from datetime import datetime

token = '1B4CDA49ECF4477CB7C7290A241EB14C'
token2 = '685DA9A1B38524471C939DEDEF0267BE'
seatNo = 'HHXYTSG20620026'
seatNo2 = 'HHXYTSG20620025'


def grab(date):
    count = 0
    while True:
        r = libraryUtils.seatDate(token, seatNo, date)
        r2 = libraryUtils.seatDate(token2, seatNo2, date)
        count += 1
        if json.loads(r)['code'] == 0:
            signTime = (int(str(date).split(',')[0]) - datetime.now().hour * 60 - datetime.now().minute) * 60 - 900
            print(signTime)
            if signTime <= 0:
                signTime = 1

            t = Timer(signTime, libraryUtils.sign, {token: token, seatNo: seatNo})
            t.start()
            print(datetime.now(), date, json.loads(r)['msg'])
            break
        elif '可能已被预约了' in json.loads(r)['msg']:
            info = libraryUtils.getUserInfoBySeat('2062', seatNo[len(seatNo) - 4:len(seatNo)])[0]
            if info is not None:
                print('{0}已经被抢了，抢座人信息:{1}'.format(seatNo, info))
                libraryUtils.autoGrab(token)
        elif count > 2000:
            break

        if json.loads(r2)['code'] == 0:
            signTime2 = (int(str(date).split(',')[0]) - datetime.now().hour * 60 - datetime.now().minute) * 60 - 900
            print(signTime2)
            if signTime2 <= 0:
                signTime2 = 1

            t2 = Timer(signTime2, libraryUtils.sign, {token: token2, seatNo: seatNo2})
            t2.start()
            print(datetime.now(), date, json.loads(r2)['msg'])
            break
        elif '可能已被预约了' in json.loads(r2)['msg']:
            info = libraryUtils.getUserInfoBySeat('2062', seatNo2[len(seatNo) - 4:len(seatNo)])[0]
            if info is not None:
                print('{0}已经被抢了，抢座人信息:{1}'.format(seatNo2, info))
                libraryUtils.autoGrab(token2)
        elif count > 2000:
            break
        print(json.loads(r)['code'])
        print(datetime.now(), date, json.loads(r)['msg'])


weekDay = str(datetime.weekday(datetime.today()))
with open('/home/ubuntu/autolibrary/mission.json') as f:
    for item in json.load(f)[weekDay]:
        grab(item)
