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
    result = utils.getUserInfoBySeat(roomID, seatID)
    return result


if __name__ == '__main__':
    app.run()
