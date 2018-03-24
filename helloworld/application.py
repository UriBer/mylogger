#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
import requests

application = Flask(__name__)

@application.route('/temp/<temp>', methods=['GET'])
def get_temp(temp):
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://freegeoip.net/json/{}'.format(user_ip) 
    response = requests.get(service_url).json()
    return Response(json.dumps({'ip address': '{}'.format(response)}), mimetype='application/json', status=200)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
