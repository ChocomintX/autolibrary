import requests
import json
from datetime import datetime
from builtins import str

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
        'seatdate': '2021-03-22'
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers, data=data)
    str = json.loads(r.text)['data']
    print(str)
    data = []
    if len(str) != 0:
        data = json.loads(str)

    result = {}
    for i in data:
        startTime = datetime.strptime(i['StartTime'], '%Y/%m/%d %H:%M:%S')
        endTime = datetime.strptime(i['EndTime'], '%Y/%m/%d %H:%M:%S')

        print(startTime)
        print(endTime)
        if startTime < datetime.now() < endTime:
            result['startTime'] = i['StartTime']
            result['endTime'] = i['EndTime']
            result['id'] = i['reader_no']
            result['department'] = i['department_name']
            result['name'] = i['real_name']

    return result
