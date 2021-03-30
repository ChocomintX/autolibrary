from flask import Flask, request
from flask_cors import CORS
from threading import Timer
import libraryUtils as utils

app = Flask(__name__)
CORS(app)


@app.route('/autolibrary/api/bindUser', methods=['POST'])
def bindUser():
    data = request.json
    print(data)
    if not utils.checkUserById(data['username']):
        return {'code': 1, 'msg': '你还没有权限使用哦'}
    results = utils.bindUser(data['username'], data['password'])
    if 'token' in results.keys():
        print(utils.unbindUser(results['token']))
    return results


@app.route('/autolibrary/api/searchSeat', methods=['POST'])
def searchSeat():
    data = request.json
    roomID = str(data['roomID'])
    seatID = str(data['seatID']).zfill(4)
    info = utils.getUserInfoBySeat(roomID, seatID)
    results = {}
    if info is not None:
        results['startTime'] = info[0]['StartTime']
        results['endTime'] = info[0]['EndTime']
        results['id'] = info[0]['reader_no']
        results['department'] = info[0]['department_name']
        results['name'] = info[0]['real_name']
    return results


@app.route('/autolibrary/api/seatDate', methods=['POST'])
def seatDate():
    data = request.json
    print(data)
    time = data['time']
    token = data['token']
    seatNo = 'HHXYTSG{0}{1}'.format(data['roomID'], str(data['seatNo']).zfill(4))
    results = utils.seatDate(token, seatNo, time)
    return results


@app.route('/autolibrary/api/autoGrab', methods=['POST'])
def autoGrab():
    data = request.json
    print(data)
    token = data['token']
    if token in utils.grabUsers and (utils.grabUsers[token]['status'] == 1 or utils.grabUsers[token]['status'] == 3):
        return {'code': 1, 'msg': '创建任务失败，已存在任务！'}

    type = int(data['type'])
    if type == 1:
        utils.grabUsers[token] = dict()
        utils.grabUsers[token]['count'] = 1
        utils.grabUsers[token]['status'] = 1
        return utils.autoGrab(token)
    else:
        roomID = data['roomID']
        seatNo = data['seatNo']
        return utils.morningGrab(token, roomID, seatNo)


@app.route('/autolibrary/api/cancelGrab', methods=['POST'])
def cancelGrab():
    token = request.json['token']
    if token in utils.grabUsers:
        utils.grabUsers.pop(token)
        return {'code': 0, 'msg': '取消抢座任务成功！'}
    else:
        return {'code': 1, 'msg': '该用户暂时没有抢座任务！'}


@app.route('/autolibrary/api/isGrab', methods=['POST'])
def isGrab():
    token = request.json['token']
    print(utils.grabUsers)
    state = utils.grabUsers.get(token)
    if state is None:
        return {'code': 1}
    else:
        return {'code': 0, 'state': state}


@app.route('/autolibrary/api/searchPeople', methods=['POST'])
def searchPeople():
    token = request.json['token']
    # print(utils.results)
    for item in utils.results.values():
        if item['status'] == 1:
            return {'code': 1, 'msg': '当前有其他用户正在使用此功能！'}

    if token not in utils.results or utils.results[token]['status'] == 0:
        name = request.json['name']
        t = Timer(1, utils.searchPeople, {token: token, name: name})
        t.start()
        return {'code': 0, 'msg': '开始搜索，请稍候刷新页面！'}
    else:
        return {'code': 1, 'msg': '正在搜索'}


@app.route('/autolibrary/api/isSearchPeople', methods=['POST'])
def isSearchPeople():
    token = request.json['token']
    if token in utils.results:
        return {'code': 0, 'results': utils.results[token]}
    else:
        return {'code': 1, 'results': []}


@app.route('/autolibrary/api/cancelSeat', methods=['POST'])
def cancelSeat():
    data = request.json
    print(data)
    token = data['token']
    type = data['type']

    print(utils.checkAdmin(token))
    if not utils.checkAdmin(token):
        return {'code': 1, 'msg': '危险功能，仅管理员可用！'}

    results = {}
    if type == 1:
        roomID = str(data['roomID'])
        seatID = str(data['seatNo']).zfill(4)
        results['data'] = utils.getUserInfoBySeat(roomID, seatID)
        results['code'] = 0
        results['msg'] = '查询状态成功！'
        return results
    else:
        id = data['id']
        return utils.cancelSeat(id, type)


@app.route('/autolibrary/api/searchUserInfo', methods=['POST'])
def searchUserInfo():
    token = request.json['token']
    return utils.searchUserInfo(token)


@app.route('/autolibrary/api/sign', methods=['POST'])
def sign():
    token = request.json['token']
    return utils.autoSign(token)


if __name__ == '__main__':
    app.run()
