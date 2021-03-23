import json

from flask import Flask, request
from flask_cors import CORS
import libraryUtils as utils

app = Flask(__name__)
CORS(app)


@app.route('/autolibrary/api/searchSeat', methods=['POST'])
def searchSeat():
    data = request.json
    roomID = str(data['roomID'])
    seatID = str(data['seatID']).zfill(4)
    results = utils.getUserInfoBySeat(roomID, seatID)
    return results


@app.route('/autolibrary/api/bindUser', methods=['POST'])
def bindUser():
    data = request.json
    results = utils.bindUser(data['username'], data['password'])
    if 'token' in results.keys():
        print(utils.unbindUser(results['token']))
    return results


@app.route('/autolibrary/api/seatDate', methods=['POST'])
def seatDate():
    data = request.json
    results = utils.seatDate(data['token'], data['seatNo'], data['time'])
    return results


@app.route('/autolibrary/api/sign', methods=['POST'])
def sign():
    data = request.json
    results = utils.sign(data['token'], data['seatNo'])
    return results


if __name__ == '__main__':
    app.run()
