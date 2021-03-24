import requests
import json
from datetime import datetime
import libraryUtils

token = '1B4CDA49ECF4477CAD2BB2781083BA62'
headers = {
    'Host': 'xzxt.hhtc.edu.cn',
    'Connection': 'keep-alive',
    'Origin': 'http://xzxt.hhtc.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html?v=20191117&seataddress=DSXYLS602&seatdate=2021-03-24&mapid=56&isloadstatus=0',
    'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
}
#
data = {
    'data_type': 'setMapPointStatus',
    'addresscode': 'DSXYLS602',
    'mapid': '56',
    'seatdate': '2021-03-24',
}

r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx', headers=headers, data=data)
print(r.text)
data = json.loads(json.loads(r.text)['data'])
print(data)

now = datetime.today()
today = "{0}-{1}-{2}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))
headers_seat = {
    'Host': 'xzxt.hhtc.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '64',
    'Accept': 'application/json',
    'Origin': 'http://xzxt.hhtc.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html?v=20191117&seataddress=DZXS306&seatdate=2021-03-24&mapid=27&isloadstatus=0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    'Cookie': 'ASP.NET_SessionId=oypn1lynbdgrfqetmn4am2ka; txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember=1B4CDA49ECF4477CF326B0E02FF26E86'
}

for item in data:
    if item['Status'] == '1':
        data_seat = {
            'data_type': 'getSeatDate',
            'seatno': item['Seat_Code'],
            'seatdate': today
        }

        r1 = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers_seat,
                           data=data_seat)
        infos = json.loads(r1.text)['data']

        print('{0}   {1}'.format(item['Seat_Code'], item['Status']))
        for info in json.loads(infos):
            print("{0}  {1}".format(info['StartTime'].split(' ')[1], info['EndTime'].split(' ')[1]))
    elif item['Status'] != '2':
        print('{0}空位！快去！'.format(item['Seat_Code']))

print(len(data))
