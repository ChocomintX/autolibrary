import json
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from threading import Timer
import libraryUtils as utils

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'hello！'


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


@app.route('/autolibrary/api/unbindUser', methods=['POST'])
def unbindUser():
    data = request.json
    utils.unbindUser(data['token'])
    utils.bindUser(data['stuNo'], data['stuNo'])
    results = utils.unbindUser(data['token'])
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
    if json.loads(results)['code'] == 0:
        signTime = (int(str(time).split(',')[0]) - datetime.now().hour * 60 - datetime.now().minute) * 60 - 900
        if signTime <= 0:
            signTime = 1
        t = Timer(signTime, utils.sign, {token: token, seatNo: seatNo})
        t.start()
    return results


@app.route('/autolibrary/api/autoGrab', methods=['POST'])
def autoGrab():
    data = request.json
    print(data)
    token = data['token']

    if not utils.checkUserByToken(token):
        return {'code': 1, 'msg': '创建任务失败，用户无权限！'}

    if token in utils.grabUsers and (utils.grabUsers[token]['status'] == 1 or utils.grabUsers[token]['status'] == 3):
        return {'code': 1, 'msg': '创建任务失败，已存在任务！'}

    type = int(data['type'])
    if type == 1:
        utils.grabUsers[token] = dict()
        utils.grabUsers[token]['count'] = 1
        utils.grabUsers[token]['status'] = 1
        roomID = data['roomID']
        return utils.autoGrab(token, roomID)
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
    token = data['token']
    type = data['type']
    check = False

    if type == 1 or 'roomID' in dict(data).keys():
        roomID = str(data['roomID'])
        seatID = str(data['seatNo']).zfill(4)
        info = utils.getUserInfoBySeat(roomID, seatID)
        questUser = utils.searchUserInfo(token)

        if info is not None:
            for item in info:
                if item['reader_no'] == json.loads(json.loads(questUser)['data'])['reader_no']:
                    check = True

    if utils.checkAdmin(token):
        check = True

    if not check:
        return {'code': 1, 'msg': '危险功能，仅管理员可用！'}

    results = {}
    if type == 1:

        results['data'] = info
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


@app.route('/autolibrary/api/getAllSeatsByUser', methods=['POST'])
def getAllSeatsByUser():
    token = request.json['token']
    return utils.getAllSeatsByUser(token)


@app.route('/autolibrary/api/getAllLocalUser', methods=['POST'])
def getAllLocalUser():
    res = dict()
    token = request.json['token']
    if utils.checkAdmin(token):
        res['data'] = utils.getAllLocalUser()
        res['code'] = 0
        res['msg'] = '查询成功！'
    else:
        res['code'] = 1
        res['msg'] = '非管理员！'
    return res


@app.route('/autolibrary/api/addLocalUser', methods=['POST'])
def addLocalUser():
    res = dict()
    token = request.json['token']
    stuNo = request.json['stuNo']
    if utils.checkAdmin(token):
        utils.addLocalUser(stuNo)
        res['code'] = 0
        res['msg'] = '添加成功！'
    else:
        res['code'] = 1
        res['msg'] = '非管理员！'
    return res


@app.route('/autolibrary/api/deleteLocalUser', methods=['POST'])
def deleteLocalUser():
    res = dict()
    token = request.json['token']
    stuNo = request.json['stuNo']
    if utils.checkAdmin(token):
        utils.deleteLocalUser(stuNo)
        res['code'] = 0
        res['msg'] = '删除成功！'
    else:
        res['code'] = 1
        res['msg'] = '非管理员！'
    return res


@app.route('/autolibrary/api/getTasks', methods=['POST'])
def getTasks():
    res = dict()
    token = request.json['token']
    if utils.checkAdmin(token):
        res['data'] = utils.getTasks()
        res['code'] = 0
        res['msg'] = '查询成功！'
    else:
        res['code'] = 1
        res['msg'] = '非管理员！'
    return res


@app.route('/autolibrary/api/deleteTask', methods=['POST'])
def deleteTask():
    res = dict()
    token = request.json['token']
    cancelToken = request.json['cancelToken']
    if utils.checkAdmin(token):
        utils.deleteTask(cancelToken)
        res['code'] = 0
        res['msg'] = '删除成功！'
    else:
        res['code'] = 1
        res['msg'] = '非管理员！'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0')
