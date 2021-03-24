import json

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
    utils.grabUsers[token] = True
    utils.autoGrab(token)

    return 'ok'


@app.route('/autolibrary/api/morningGrab', methods=['POST'])
def morningGrab():
    data = request.json
    print(data)
    token = data['token']
    utils.grabUsers[token] = True
    utils.autoGrab(token)

    return 'ok'

@app.route('/test1')
def test1():
    utils.grabUsers['321'] = 1
    print('321' in utils.grabUsers)
    return json.dumps(utils.grabUsers)


@app.route('/test2')
def test2():
    utils.grabUsers['123'] = 2
    return json.dumps(utils.grabUsers)


if __name__ == '__main__':
    app.run()
