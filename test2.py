from threading import Timer
import libraryUtils
import json

# def grap():
#     while True:
#         r = libraryUtils.seatDate('1B4CDA49ECF4477CB7C7290A241EB14C', 'HHXYTSG20620026', '510,1320')
#         print(json.loads(r)['code'])
#         if json.loads(r)['code'] != 1:
#             break
#
#
# t = Timer(19800, grap)
# t.start()

a = [{'Area_Code': 'HHXY01', 'Code': 'XKYS102', 'Name': '西区开放学习室1-2', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '30', 'Quantity': '32', 'status0': '19', 'status1': '1', 'status2': '12', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XKYS101', 'Name': '西区学习室1-1', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '29', 'Quantity': '48', 'status0': '32', 'status1': '0', 'status2': '16', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XZXS301', 'Name': '西区学习室3-1', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '14', 'Quantity': '95', 'status0': '53', 'status1': '1', 'status2': '41', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XZXS302', 'Name': '西区学习室3-2', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '15', 'Quantity': '149', 'status0': '87', 'status1': '3', 'status2': '59', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XZXS401', 'Name': '西区学习室4-1', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '16', 'Quantity': '95', 'status0': '54', 'status1': '0', 'status2': '41', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XZXS402', 'Name': '西区学习室4-2', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '17', 'Quantity': '151', 'status0': '60', 'status1': '0', 'status2': '91', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY01', 'Code': 'XZXS201', 'Name': '西区电子阅览室', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '84', 'Quantity': '54', 'status0': '1', 'status1': '4', 'status2': '49', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS201', 'Name': '东区学习室2-1', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '19', 'Quantity': '108', 'status0': '26', 'status1': '2', 'status2': '80', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS202', 'Name': '东区学习室2-2', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '20', 'Quantity': '108', 'status0': '24', 'status1': '1', 'status2': '83', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS204', 'Name': '东区学习室2-4', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '21', 'Quantity': '74', 'status0': '22', 'status1': '1', 'status2': '51', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS301', 'Name': '东区学习室3-1', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '22', 'Quantity': '108', 'status0': '32', 'status1': '8', 'status2': '68', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS302', 'Name': '东区学习室3-2', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '23', 'Quantity': '108', 'status0': '25', 'status1': '7', 'status2': '76', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS303', 'Name': '东区学习室3-3', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '24', 'Quantity': '74', 'status0': '14', 'status1': '4', 'status2': '56', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS304', 'Name': '东区学习室3-4', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '25', 'Quantity': '74', 'status0': '22', 'status1': '2', 'status2': '50', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS305', 'Name': '东区学习室3-5', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '26', 'Quantity': '170', 'status0': '63', 'status1': '5', 'status2': '102', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZXS306', 'Name': '东区学习室3-6', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '27', 'Quantity': '251', 'status0': '85', 'status1': '6', 'status2': '160', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DZX601', 'Name': '东区6楼电子阅览室', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '83', 'Quantity': '153', 'status0': '25', 'status1': '3', 'status2': '125', 'IsLoadMapStatus': '0'},
     {'Area_Code': 'HHXY02', 'Code': 'DSXYLS602', 'Name': '东区6楼声像阅览室', 'StartTime': '07:00:00', 'EndTime': '22:00:00',
      'Map_Id': '56', 'Quantity': '126', 'status0': '1', 'status1': '2', 'status2': '123', 'IsLoadMapStatus': '0'}]

l = []
for i in a:
    t = {'addresscode': i['Code'], 'mapid': i['Map_Id']}
    t1 = {'key': i['Name'], 'value': t}
    l.append(t1)

print(l)
