import requests
import json
from datetime import datetime

roomIDs = {
    "东区学习室2-1": "2021",
    "东区学习室2-2": "2022",
    "东区学习室2-4": "2024",
    "东区学习室3-1": "2031",
    "东区学习室3-2": "2032",
    "东区学习室3-3": "2033",
    "东区学习室3-4": "2034",
    "东区学习室3-6": "2036",
    "东区6楼电子阅览室": "2063",
    "东区6楼声像阅览室": "2062"
}


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
        'Cookie': 'ASP.NET_SessionId=oypn1lynbdgrfqetmn4am2ka; txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember=1B4CDA49ECF4477CF326B0E02FF26E86'
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

    result = {}
    for i in data:
        startTime = datetime.strptime(i['StartTime'], '%Y/%m/%d %H:%M:%S')
        endTime = datetime.strptime(i['EndTime'], '%Y/%m/%d %H:%M:%S')

        if startTime < datetime.now() < endTime:
            result['startTime'] = i['StartTime']
            result['endTime'] = i['EndTime']
            result['id'] = i['reader_no']
            result['department'] = i['department_name']
            result['name'] = i['real_name']

    return result


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
        'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/bind.html?v=20210323101246',
        'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; txw_cookie_wxuser_model=AB02FFC31FF35CC1D5615DAD48C0B3E8D64FB22662DCD3BFBE04A088CC7E09AA23CAC2895E798E94EA4EB57C3707261FB521CC415FBC12B0E256A9BBEB3C7808A8CB779C2B1616C8AEF2F3F67270EA67E68C57A3AAAC051DC4245DE8B4E17CA87A3D2782A48E7B6D218DC193727DE8C26A2CF4A043DEFA4373EE2EE52B27A8FCC254BCC3D78AD23D07A03040C2E02B8678B668D8245B0AB5623DFA7A07814B0971704F8DB20CFD8F44D32A191482B43876D4821CA35C9A31089DE79D224D3C6AD4C163B9BAF10ADD6F21147B2E3ED1DD1C44E651D283CC070A2E55983098D8396330EA75365EA5251015D8F799EC127396EE1A9D92A026EB82DA82D73ED2F0EE1087BF80C76AA2BE10A89C60A336861CDD768780455CED8231DC20A7B2F4DDB2DF03FA7E284BF00C4A147E3D01DF65D2185EB0ECD39865C678E5152B293435DAE170C9BEB77D0FF76FE2426D3E01F0C69E7AA50973990CAC9D034D65C6C73A92E5A5E2A455DDC2DE58539191FBC2EFD965C52D1BD97C3C417E5E3F4A47E563D225344E9981D8B0C4B0DED4F39C6011155F5E64B707346CB133D6D02DE86272D0FC02595CD78382A77E24D8A34E38DC54C91F6CBDB7DDDE78'
    }

    data = {
        'data_type': 'bindUser',
        'readerno': username,
        'unitid': '6',
        'department': '111',
        'passwd': password,
        'tel': '13187279968'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/basic/UserHandler.ashx', headers=headers, data=data)
    results = json.loads(r.text)

    if results['code'] == 0:
        results['token'] = r.cookies['dt_cookie_user_name_remember']

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
