# -*- coding: UTF-8 -*-
from flask import Flask, render_template, Response
from flask_cors import CORS
import json
import requests
import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from plugin import processSpecial as PS
#from plugin import processSpecial
app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/location')
def get_location():
    r = {
        "type": "FeatureCollection",
        "features": [

        ]
    }
    j = requests.get(
        'https://www.nlpi.edu.tw/opendata/da08aaaf-7edd-461d-a645-3039f840a1a8', verify=False)

    for l in j.json():
        if l['經度'] != '' and l['緯度'] != '':
            r['features'].append(
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(l['經度']),
                            float(l['緯度'])
                        ]
                    },
                    "type": "Feature"
                }
            )
    return Response(json.dumps(r), mimetype='application/json')


@app.route('/getUniversityLib')
def getUniversityLib():
    data = PS.universityLibary()
    r = {
        'status': '200',
        'time': str(datetime.datetime.now()),
        'data': data
    }
    print("status:", '200')
    return Response(json.dumps(r), mimetype='application/json')


@app.route('/getLibary')
def getLibary():
    data = PS.libaryCombie()
    r = {
        'status': '200',
        'time': str(datetime.datetime.now()),
        'data': data
    }
    print("status:", '200')
    return Response(json.dumps(r), mimetype='application/json')


@app.route('/getSchools')
def getSchools():
    data = PS.schoolCombine()
    r = {
        'status': '200',
        'time': str(datetime.datetime.now()),
        'data': data
    }
    print("status:", '200')
    return Response(json.dumps(r), mimetype='application/json')
# for test url
@app.route('/testData')
def test():
    testUrl = "https://quality.data.gov.tw/dq_download_json.php?nid=8306&md5_url=3a7adaba0bca31a3d39903357acc8a0c"
    res = requests.get(testUrl)
    r = {
        'status': res.status_code,
        'time': str(datetime.datetime.now()),
        'data': res.json()
    }
    print("status:", res.status_code)
    return Response(json.dumps(r), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=1125)
