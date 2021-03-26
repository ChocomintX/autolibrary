import json

from flask import Flask, request
from flask_cors import CORS
from threading import Timer
from datetime import datetime
import libraryUtils as utils

app = Flask(__name__)
CORS(app)


@app.route('/autolibrary/api/bindUser', methods=['POST'])
def bindUser():
    data = request.json
    print(data)
    if data['pycode'] != '1800130935':
        return {'code': 1, 'msg': 'py码不对！'}
    results = utils.bindUser(data['username'], data['password'])
    if 'token' in results.keys():
        print(utils.unbindUser(results['token']))
    return results


@app.route('/autolibrary/api/searchSeat', methods=['POST'])
def searchSeat():
    data = request.json
    roomID = str(data['roomID'])
    seatID = str(data['seatID']).zfill(4)
    results = utils.getUserInfoBySeat(roomID, seatID)
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


@app.route('/autolibrary/api/sign', methods=['POST'])
def sign():
    data = request.json
    results = utils.sign(data['token'], data['seatNo'])
    return results


@app.route('/autolibrary/api/autoGrab', methods=['POST'])
def autoGrab():
    data = request.json
    print(data)
    token = data['token']
    if token in utils.grabUsers and (utils.grabUsers[token]['status'] == 1 or utils.grabUsers[token]['status'] == 3):
        return {'code': 1, 'msg': '创建任务失败，已存在任务！'}

    type = int(data['type'])
    utils.grabUsers[token] = dict()
    utils.grabUsers[token]['count'] = 1
    if type == 1:
        utils.grabUsers[token]['status'] = 1
        return utils.autoGrab(token)
    else:
        utils.grabUsers[token]['status'] = 3
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
    token = request.json['token']
    return {'code': 0, 'msg': '危险功能，不准用！'}


if __name__ == '__main__':
    app.run()
