import libraryUtils
import json

js = {'685DA9A1B385244750117C9DA05495F9': {'count': 137, 'status': 0, 'seatNo': 'HHXYTSG20620093', 'msg': '抢座 成功！'},
      '1B4CDA49ECF4477CF326B0E02FF26E86': {'count': 185, 'status': 0, 'seatNo': 'HHXYTSG20620036', 'msg': '抢座成功！'},
      '685DA9A1B3852447DDA219F67B9D4236': {'count': 169, 'status': 0, 'seatNo': 'HHXYTSG20620031', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477C1CE2BBC3C9AC92F6': {'count': 160, 'status': 0, 'seatNo': 'HHXYTSG20620033', 'msg': '抢座成功！'},
      '685DA9A1B38524474752EB1540611AD5': {'count': 1, 'status': 0},
      '1B4CDA49ECF4477C0133AFA68A9E749C': {'count': 127, 'status': 0, 'seatNo': 'HHXYTSG20620009', 'msg': '抢座成功！'},
      '2D2AF7A9FEDDCD419A2C8F604EDDBBFD': {'count': 246, 'status': 2, 'seatNo': 'HHXYTSG20620080',
                                           'msg': '预约失败，该时段可能已被预约了，请刷新地图重试'},
      '685DA9A1B3852447174FF8DF868A71FD': {'count': 178, 'status': 0, 'seatNo': 'HHXYTSG20620032', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477C9E079E6EC4B62FA3': {'count': 1, 'status': 3, 'seatNo': 'HHXYTSG20620044'},
      '685DA9A1B3852447DCD5C61289E42418': {'count': 168, 'status': 0, 'seatNo': 'HHXYTSG20620069', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477C8A30FDCE599C4137': {'count': 674, 'status': 2, 'seatNo': 'HHXYTSG20620044', 'msg': '您已预约该时段'},
      '1B4CDA49ECF4477CD46B06A3C8FA9969': {'count': 179, 'status': 0, 'seatNo': 'HHXYTSG20620045', 'msg': '抢座成功！'},
      '685DA9A1B38524477DF224A65ED01527': {'count': 121, 'status': 0, 'seatNo': 'HHXYTSG20620007', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477CCD180C190413BA7D': {'count': 141, 'status': 0, 'seatNo': 'HHXYTSG20620034', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477CACD0C76B8147FB4E': {'count': 1309, 'status': 0},
      '685DA9A1B3852447156E348876B81AD0': {'count': 933, 'status': 2, 'msg': '预约失败，该时段可能已被预约了，请刷新地图重试'},
      '1B4CDA49ECF4477C671B41287E9CE992': {'count': 766, 'status': 0, 'seatNo': 'HHXYTSG20620082', 'msg': '抢座成功！'},
      '2D2AF7A9FEDDCD41D84C6A1814551424': {'count': 1883, 'status': 0, 'seatNo': 'HHXYTSG20620083', 'msg': '抢座成功！'},
      '2D2AF7A9FEDDCD415CCC8139E68A6E79': {'count': 149, 'status': 0, 'seatNo': 'HHXYTSG20620084', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477CBE9B423DAE6B1B95': {'count': 149, 'status': 0, 'seatNo': 'HHXYTSG20620086', 'msg': '抢座成功！'},
      '685DA9A1B38524478CDDCD5D3FAB6AF2': {'count': 812, 'status': 0, 'seatNo': 'HHXYTSG20620019', 'msg': '抢座成功！'},
      '685DA9A1B3852447B1DD385B6C73EB13': {'count': 755, 'status': 0, 'seatNo': 'HHXYTSG20620058', 'msg': '抢座成功！'},
      '1B4CDA49ECF4477C98C79B7064AAA30C': {'count': 300, 'status': 1}}

with open('./config.json') as r:
    tokens = json.load(r);
    for k in js.keys():
        data = json.loads(json.loads(libraryUtils.searchUserInfo(k))['data'])
        print(data['real_name'])
        print(data['reader_no'])
