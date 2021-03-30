import requests
import json
from datetime import datetime
import libraryUtils

roomInfo = [{'name': '西区开放学习室1-2', 'num': '32', 'roomID': '1012', 'mapId': '30', 'code': 'XKYS102'},
            {'name': '西区学习室1-1', 'num': '48', 'roomID': '1011', 'mapId': '29', 'code': 'XKYS101'},
            {'name': '西区学习室3-1', 'num': '95', 'roomID': '1031', 'mapId': '14', 'code': 'XZXS301'},
            {'name': '西区学习室3-2', 'num': '149', 'roomID': '1032', 'mapId': '15', 'code': 'XZXS302'},
            {'name': '西区学习室4-1', 'num': '95', 'roomID': '1041', 'mapId': '16', 'code': 'XZXS401'},
            {'name': '西区学习室4-2', 'num': '151', 'roomID': '1042', 'mapId': '17', 'code': 'XZXS402'},
            {'name': '西区电子阅览室', 'num': '54', 'roomID': '1021', 'mapId': '84', 'code': 'XZXS201'},
            {'name': '东区学习室2-1', 'num': '108', 'roomID': '2021', 'mapId': '19', 'code': 'DZXS201'},
            {'name': '东区学习室2-2', 'num': '108', 'roomID': '2022', 'mapId': '20', 'code': 'DZXS202'},
            {'name': '东区学习室2-4', 'num': '74', 'roomID': '2024', 'mapId': '21', 'code': 'DZXS204'},
            {'name': '东区学习室3-1', 'num': '108', 'roomID': '2031', 'mapId': '22', 'code': 'DZXS301'},
            {'name': '东区学习室3-2', 'num': '108', 'roomID': '2032', 'mapId': '23', 'code': 'DZXS302'},
            {'name': '东区学习室3-3', 'num': '74', 'roomID': '2033', 'mapId': '24', 'code': 'DZXS303'},
            {'name': '东区学习室3-4', 'num': '74', 'roomID': '2034', 'mapId': '25', 'code': 'DZXS304'},
            {'name': '东区学习室3-5', 'num': '170', 'roomID': '2035', 'mapId': '26', 'code': 'DZXS305'},
            {'name': '东区学习室3-6', 'num': '251', 'roomID': '2036', 'mapId': '27', 'code': 'DZXS306'},
            {'name': '东区6楼电子阅览室', 'num': '153', 'roomID': '2063', 'mapId': '83', 'code': 'DZX601'},
            {'name': '东区6楼声像阅览室', 'num': '126', 'roomID': '2062', 'mapId': '56', 'code': 'DSXYLS602'}]
roomInfo.reverse()
searchUser = []

results = {'count': 0, 'list': []}
size = 1978

now = datetime.today()
today = "{0}-{1}-{2}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

token = '1B4CDA49ECF4477CAD2BB2781083BA62'
headers = {
    'Host': 'xzxt.hhtc.edu.cn',
    'Connection': 'keep-alive',
    'Origin': 'http://xzxt.hhtc.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://xzxt.hhtc.edu.cn/mobile/html/seat/seatdate.html',
    'Cookie': 'txw_cookie_txw_unit_Id=968131EA0968E222; dt_cookie_user_name_remember={0}'.format(token)
}

start = datetime.now()

for room in roomInfo:
    data = {
        'data_type': 'setMapPointStatus',
        'addresscode': room['code'],
        'mapid': room['mapId'],
        'seatdate': today,
    }

    r = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx', headers=headers, data=data)
    print(r.text)
    data = json.loads(json.loads(r.text)['data'])

    for item in data:
        results['count'] += 1
        print(results['count'])
        if item['Status'] != '0':
            data_seat = {
                'data_type': 'getSeatDate',
                'seatno': item['Seat_Code'],
                'seatdate': today
            }
            try:
                r1 = requests.post('http://xzxt.hhtc.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', headers=headers,
                                   data=data_seat)
                infos = json.loads(r1.text)['data']

                for info in json.loads(infos):
                    if '覃婧' in info['real_name']:
                        results['list'].append(info)
            except:
                print('error')
                continue

end = datetime.now()
print(start, end, end - start)
print(results)
