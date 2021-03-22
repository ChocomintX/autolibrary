import requests
import json
from datetime import datetime

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
    'seatno': 'HHXYTSG20620095',
    'seatdate': '2021-03-22'
}

r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers, data=data)
print(json.loads(r.text)['data'])
data = json.loads(json.loads(r.text)['data'])
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

print(json.dumps(result))
