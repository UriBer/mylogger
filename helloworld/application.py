#!flask/bin/python
import json
from flask import Flask, Response, request, render_template
from helloworld.flaskrun import flaskrun
#from helloworld.bl import ip_meta
import requests
import boto3
import datetime

application = Flask(__name__)

@application.route('/temp/<temp>', methods=['GET'])
def get_temp(temp):
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://freegeoip.net/json/{}'.format(user_ip) 
    response = requests.get(service_url).json()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('eb_logger_log')
    res_data = {k: v for k, v in response.items() if v!=''}
    print(res_data)
    
    table.put_item(
    Item={
        'path': temp,
        'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ip_meta' : res_data
         }
    )
    
    #return render_template('index.html', title='Stats', response=response) 
    return Response(json.dumps({'ip address': '{}'.format(response)}), mimetype='application/json', status=200)

'''
@application.route('/tst/<temp>', methods=['GET'])
def tst_temp(temp):
    user_ip = str(request.environ['REMOTE_ADDR'])
    return (ip_meta(user_ip, temp))
'''
@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
