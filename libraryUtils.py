import requests
import json
from datetime import datetime, timedelta
from threading import Timer
import mailUtils

grabUsers = dict()
results = {'empty': {'count': 0, 'list': [], 'status': 0}}

roomInfo = [{'name': '东区6楼声像阅览室', 'num': '126', 'roomID': '2062', 'mapId': '56', 'code': 'DSXYLS602'},
            {'name': '东区6楼电子阅览室', 'num': '153', 'roomID': '2063', 'mapId': '83', 'code': 'DZX601'},
            {'name': '东区学习室3-6', 'num': '251', 'roomID': '2036', 'mapId': '27', 'code': 'DZXS306'},
            {'name': '东区学习室3-5', 'num': '170', 'roomID': '2035', 'mapId': '26', 'code': 'DZXS305'},
            {'name': '东区学习室3-4', 'num': '74', 'roomID': '2034', 'mapId': '25', 'code': 'DZXS304'},
            {'name': '东区学习室3-3', 'num': '74', 'roomID': '2033', 'mapId': '24', 'code': 'DZXS303'},
            {'name': '东区学习室3-2', 'num': '108', 'roomID': '2032', 'mapId': '23', 'code': 'DZXS302'},
            {'name': '东区学习室3-1', 'num': '108', 'roomID': '2031', 'mapId': '22', 'code': 'DZXS301'},
            {'name': '东区学习室2-4', 'num': '74', 'roomID': '2024', 'mapId': '21', 'code': 'DZXS204'},
            {'name': '东区学习室2-2', 'num': '108', 'roomID': '2022', 'mapId': '20', 'code': 'DZXS202'},
            {'name': '东区学习室2-1', 'num': '108', 'roomID': '2021', 'mapId': '19', 'code': 'DZXS201'},
            {'name': '西区电子阅览室', 'num': '54', 'roomID': '1021', 'mapId': '84', 'code': 'XZXS201'},
            {'name': '西区学习室4-2', 'num': '151', 'roomID': '1042', 'mapId': '17', 'code': 'XZXS402'},
            {'name': '西区学习室4-1', 'num': '95', 'roomID': '1041', 'mapId': '16', 'code': 'XZXS401'},
            {'name': '西区学习室3-2', 'num': '149', 'roomID': '1032', 'mapId': '15', 'code': 'XZXS302'},
            {'name': '西区学习室3-1', 'num': '95', 'roomID': '1031', 'mapId': '14', 'code': 'XZXS301'},
            {'name': '西区学习室1-1', 'num': '48', 'roomID': '1011', 'mapId': '29', 'code': 'XKYS101'},
            {'name': '西区开放学习室1-2', 'num': '32', 'roomID': '1012', 'mapId': '30', 'code': 'XKYS102'}]


def getToday():
    now = datetime.today()
    today = "{0}-{1}-{2}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))
    return today


def getUserInfoBySeat(roomID, seatID):
    seatNo = 'HHXYTSG{0}{1}'.format(roomID, seatID)

    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '64',
        'Accept': 'application/json',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html?v=20191117&seataddress=DZXS306&seatdate=2021-03-22&mapid=27&isloadstatus=0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
        'Cookie': 'ASP.NET_SessionId=oypn1lynbdgrfqetmn4am2ka; txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember=1B4CDA49ECF4477C51F03D5B15B04311'
    }

    data = {
        'data_type': 'getSeatDate',
        'seatno': seatNo,
        'seatdate': getToday()
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers, data=data)
    infos = json.loads(r.text)['data']
    data = []
    if len(infos) != 0:
        data = json.loads(infos)
        # print(data)
        return data

    # for i in data:
    #     startTime = datetime.strptime(i['StartTime'], '%Y/%m/%d %H:%M:%S')
    #     endTime = datetime.strptime(i['EndTime'], '%Y/%m/%d %H:%M:%S')
    #
    #     if startTime < datetime.now() < endTime:
    #         result['startTime'] = i['StartTime']
    #         result['endTime'] = i['EndTime']
    #         result['id'] = i['reader_no']
    #         result['department'] = i['department_name']
    #         result['name'] = i['real_name']
    #         return i
    return None


def bindUser(username, password):
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '96',
        'Accept': 'application/json',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/bind.html?v=20210323090911',
        'Cookie': 'ASP.NET_SessionId=yqp3yofc5s0zegathhml1zwi; txw_cookie_txw_unit_Id=968131EA0968E222; txw_cookie_wxuser_model=AB02FFC31FF35CC1D5615DAD48C0B3E8D64FB22662DCD3BFBE04A088CC7E09AA23CAC2895E798E9405FC4EF34A955A0DC64FBDD3EEB287FED2154ADD502AEEF9A6101B078EA1314341B32772E757758B87E458DDED66D210D1CB57AE1B9313299657B9301DBF45336D83CEFE93F902045F2846BE42802D881DB211706D5950BF0E80E8B61AD2EC937C9CC5B2506B71E7CA8BE4F7CFD9EBF57D5DBA8A6E3E53AC4706777CA0B3EDC9A7A749752B86744734201F6296377A472C97809E6AEA6BB61342C2904C3625F6555C4FD58E090A7E9FA3892770AFDB0E60605AACCE8A27C020E14035E2AD97A75202C913DCD7A151D09A40DB6317AEF8233942E7C6E4DDA61A868E2F684FAF95B84D72F80DD4AD8F78B4F98E7DCFDB13891F852EE53BF9DA9DD1662C598AAF23'
    }

    data = {
        'data_type': 'bindUser',
        'readerno': username,
        'unitid': '6',
        'department': '111',
        'passwd': password,
        'tel': '13185479944'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/basic/UserHandler.ashx', headers=headers, data=data)
    results = json.loads(r.text)

    if results['code'] == 0:
        results['token'] = r.cookies['dt_cookie_user_name_remember']

        with open('./config.json', 'r') as f:
            config = json.load(f)

        with open('./config.json', 'w') as f:
            config['users'][username]['token'] = results['token']
            config['users'][username]['password'] = password
            f.write(json.dumps(config))

        # mailUtils.sendEmail('新用户登录', '用户名：{0}  \n密码：{1}  \ntoken：{2}'.format(username, password,
        #                                                                      r.cookies['dt_cookie_user_name_remember']))s
    return results


def unbindUser(token):
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/usercenter/my.html?v=20191117',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    data = {
        'data_type': 'unbindUser'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/basic/UserHandler.ashx', headers=headers, data=data)

    return r.text


def seatDate(token, seatNo, time):
    # token = '1B4CDA49ECF4477C9DFCAC8D6CC9626F'
    # dateTime = '1079,1200'
    # seatNo = 'HHXYTSG20350151'
    date = getToday()

    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html?v=20191117&seataddress=DSXYLS602&seatdate=2021-03-23&mapid=56&isloadstatus=0',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    data = {
        "data_type": "seatDate",
        "seatno": seatNo,
        "seatdate": date,
        "datetime": time,
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers, data=data)
    return r.text


def sign(token, seatNo):
    # token = '1B4CDA49ECF4477CAC6A549271936426'
    # seatNo = 'HHXYTSG10420012'
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/index.html?v=20210323162222',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    data = {
        "data_type": "scanSign",
        "barcode": seatNo
    }
    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/ScanHandler.ashx', headers=headers, data=data)
    return r.text


def autoGrab(token, roomID):
    date = getToday()
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html?v=20191117&seataddress=DSXYLS602&seatdate=2021-03-24&mapid=56&isloadstatus=0',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    for item in roomInfo:
        if item['roomID'] == roomID:
            addresscode = item['code']
            mapid = item['mapId']
            # print(addresscode, mapid)

    data = {
        'data_type': 'setMapPointStatus',
        'addresscode': addresscode,
        'mapid': mapid,
        'seatdate': date,
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx', headers=headers, data=data)
    data = json.loads(json.loads(r.text)['data'])
    for item in data:
        if item['Status'] == '0':
            time = '{0},{1}'.format(datetime.now().hour * 60 + datetime.now().minute + 10, 1320)
            mSeat = json.loads(seatDate(token, item['Seat_Code'], time))
            if mSeat['code'] == 0:
                grabUsers[token]['status'] = 0
                print('已预约，座位号{0}'.format(item['Seat_Code']))
                mSign = json.loads((sign(token, item['Seat_Code'])))['code']
                if mSign == 0:
                    print('已签到')
                break
            else:
                grabUsers[token]['status'] = 2
                grabUsers[token]['msg'] = mSeat['msg']
                print(mSeat)

    if token in grabUsers and grabUsers.get(token)['status'] == 1:
        grabUsers[token]['count'] += 1
        t = Timer(1, autoGrab, {token: token, roomID: roomID})
        t.start()
    return {'code': 0, 'msg': '任务创建成功'}


def morningGrab(token, roomID, seatNo):
    seatNo = 'HHXYTSG' + roomID + str(seatNo).zfill(4)
    if seatNo == 'HHXYTSG20620026' and not checkAdmin(token):
        return {'code': 1, 'msg': '管理员坐的座位就别抢了吧哥哥'}
    else:
        for item in grabUsers.values():
            if item['status'] == 3 and item['seatNo'] == seatNo:
                return {'code': 1, 'msg': '这个座位有人预约了，换一个吧'}

    grabUsers[token] = dict()
    grabUsers[token]['count'] = 1
    grabUsers[token]['status'] = 3
    grabUsers[token]['seatNo'] = seatNo

    now = datetime.now()
    if 6 > now.hour >= 0:
        grabTime = datetime(now.year, now.month, now.day, 5, 59, 59)
    else:
        grabTime = datetime(now.year, now.month, now.day, 5, 59, 59) + timedelta(days=1)

    def grab(tk, sn):
        if grabUsers['seatNo'] != sn:
            return
        grabUsers[token]['status'] = 1
        now = datetime.now() + timedelta(minutes=3)
        while now > datetime.now():
            r = seatDate(tk, sn, '420,1320')
            print(json.loads(r))
            if json.loads(r)['code'] == 0 or token not in grabUsers:
                grabUsers[token]['status'] = 0
                grabUsers[token]['msg'] = '抢座成功！'
                st = Timer(3600, sign, {token: tk, seatNo: sn})
                st.start()
                break
            elif '可能已被预约了' in json.loads(r)['msg']:
                info = getUserInfoBySeat(roomID, seatNo[len(seatNo) - 4:len(seatNo)])[0]
                if info is not None:
                    print('预约失败,开始自动抢座')
                    autoGrab(token, roomID)
                    # print('{0}已经被抢了，抢座人信息:{1}'.format(sn, info))
                    # if not checkUserById(info['reader_no']):
                    #     print('取消原本{0}的预约'.format(sn))
                    #     cancelSeat(info['Id'], 3)
                    #     cancelSeat(info['Id'], 2)
            elif json.loads(r)['code'] == 1:
                grabUsers[token]['count'] += 1

        # if grabUsers[token]['status'] == 1:
        #     print('预约失败,开始自动抢座')
        #     autoGrab(token, roomID)

    seconds = (grabTime - now).seconds
    t = Timer(seconds, grab, {token: token, seatNo: seatNo})
    t.start()
    return {'code': 0, 'msg': '任务创建成功'}


# def morningGrab2(token, roomID, seatNo):
#     seatNo = 'HHXYTSG' + roomID + str(seatNo).zfill(4)
#     if seatNo == 'HHXYTSG20620026' and not checkAdmin(token):
#         return {'code': 1, 'msg': '管理员坐的座位就别抢了吧哥哥'}
#     else:
#         for item in grabUsers.values():
#             if item['status'] == 3 and item['seatNo'] == seatNo:
#                 return {'code': 1, 'msg': '这个座位有人预约了，换一个吧'}
#
#     grabUsers[token] = dict()
#     grabUsers[token]['count'] = 1
#     grabUsers[token]['status'] = 3
#     grabUsers[token]['seatNo'] = seatNo
#
#     now = datetime.now()
#     if 6 > now.hour >= 0:
#         grabTime = datetime(now.year, now.month, now.day, 5, 59, 59)
#     else:
#         grabTime = datetime(now.year, now.month, now.day, 5, 59, 59) + timedelta(days=1)
#
#     def grab(tk, sn):
#         grabUsers[token]['status'] = 1
#         now = datetime.now() + timedelta(seconds=5)
#         while now > datetime.now():
#
#             r = seatDate(tk, sn, '600,1439')
#             if json.loads(r)['code'] == 0 or token not in grabUsers:
#                 grabUsers[token]['status'] = 0
#                 grabUsers[token]['msg'] = '抢座成功！'
#                 st = Timer(14400, sign, {token: tk, seatNo: sn})
#                 st.start()
#                 break
#             elif '可能已被预约了' in json.loads(r)['msg']:
#                 info = getUserInfoBySeat(roomID, seatNo[len(seatNo) - 4:len(seatNo)])[0]
#                 print('{0}已经被抢了，抢座人信息:{1}'.format(sn, info))
#                 if not checkUserById(info['reader_no']):
#                     print('取消原本{0}的预约'.format(sn))
#                     # cancelSeat(info['Id'], 3)
#             elif json.loads(r)['code'] == 1:
#                 grabUsers[token]['count'] += 1
#
#         if grabUsers[token]['status'] == 1:
#             # autoGrab(token)
#             print('运行自动抢座')
#
#     seconds = (grabTime - now).seconds
#     t = Timer(1, grab, {token: token, seatNo: seatNo})
#     t.start()
#     return {'code': 0, 'msg': '任务创建成功'}


def searchPeople(token, name):
    # size = 1978
    today = getToday()
    results[token] = {'count': 0, 'list': [], 'status': 1}

    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }
    errorlist = []
    sum = 0
    for room in roomInfo:
        data = {
            'data_type': 'setMapPointStatus',
            'addresscode': room['code'],
            'mapid': room['mapId'],
            'seatdate': today,
        }

        i = 0
        while i < 5:
            try:
                r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx', headers=headers,
                                  data=data)
                data = json.loads(json.loads(r.text)['data'])
                i = 5
            except:
                errorlist.append(room)
                i += 1

        for item in data:
            results[token]['count'] += 1
            if item['Status'] != '0':
                data_seat = {
                    'data_type': 'getSeatDate',
                    'seatno': item['Seat_Code'],
                    'seatdate': today
                }

                j = 0
                while j < 5:
                    try:
                        r1 = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                                           headers=headers,
                                           data=data_seat)
                        infos = json.loads(r1.text)['data']

                        for info in json.loads(infos):
                            if name in info['real_name']:
                                results[token]['list'].append(info)
                        j = 5
                    except:
                        errorlist.append(item)
                        j += 1
    results[token]['status'] = 0
    return sum


def searchUserInfo(token):
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/usercenter/person_info.html',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    data = {
        'data_type': 'user_info'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/user/UserHandler.ashx', headers=headers, data=data)

    return r.text


def autoSign(token):
    l = json.loads(getAllSeatsByUser(token))
    if len(l) > 0:
        return sign(token, l[0]['SeatInfo_Code'])


def getAllSeatsByUser(token):
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Connection': 'keep-alive',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seat_record.html',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
    }

    data = {
        'page': 1,
        'size': 10,
        'data_type': 'seat_date_list'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatRecordHandler.ashx', headers=headers, data=data)
    return r.text


def cancelSeat(id, type):
    headers = {
        'Host': 'xzxt.hhtc.edu.cn',
        'Origin': 'http://xzxt.hhtc.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seat_record.html',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember=' +
                  '1B4CDA49ECF4477CAC6A549271936426'
    }

    data_type = ''
    submitUrl = ''
    if int(type) == 2:
        data_type = 'signOut'
        submitUrl = 'http://xzxt.hhtc.edu.cn/mobile/ajax/seat/ScanHandler.ashx'
    elif int(type) == 3:
        data_type = 'cancel_seat_date'
        submitUrl = 'http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx'
    data = {
        'data_type': data_type,
        'id': id
    }

    r = requests.post(submitUrl, headers=headers, data=data)
    print(data)
    return r.text


def checkAdmin(token):
    config = json.load(open('./config.json'))
    return token in config['admin'].values()


def checkUserByToken(token):
    with open('./config.json', 'r') as f:
        config = json.load(f)
        for user in config['users'].values():
            if token == user['token']:
                return True
        return False


def checkUserById(id):
    with open('./config.json', 'r') as f:
        config = json.load(f)
        return str(id) in config['users'].keys()


def getAllLocalUser():
    with open('./config.json', 'r') as f:
        users = json.load(f)['users']
        print(users)
        res = []
        for i in users:
            item = users[i]
            item['stuNo'] = i
            res.append(item)
        return res


def addLocalUser(stuNo):
    with open('./config.json', 'r') as f:
        config = json.load(f)
    with open('./config.json', 'w') as f:
        config['users'][stuNo] = {}
        f.write(json.dumps(config))


def deleteLocalUser(stuNo):
    with open('./config.json', 'r') as f:
        config = dict(json.load(f))
    with open('./config.json', 'w') as f:
        # print(config)
        config.pop(stuNo)
        f.write(json.dumps(config))
