# append to path in dev, in prod it's part of the path
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from flask import Flask, Response, request, render_template
from helloworld.flaskrun import flaskrun
import requests
import datetime
import json
import boto3


application = Flask(__name__)


@application.route('/test/<temp>', methods=['GET'])
def get_test(temp):
    response = get_ip_meta()
    return Response(json.dumps({'ip address': '{}'.format(response)}), mimetype='application/json', status=200)


@application.route('/page/<temp>', methods=['GET'])
def get_page(temp):
    response = get_ip_meta()
    return render_template('index.html', response=response, title=temp)
    #Response(json.dumps({'ip address': '{}'.format(response)}), mimetype='application/json', status=200)


@application.route('/temp/<temp>', methods=['GET'])
def get_temp(temp):
    response = get_ip_meta()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('eb_logger_log')
    res_data = {k: v for k, v in response.items() if v!=''}
    print(res_data)
    item={
    'path': temp,
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'ip_meta' : res_data
     }
    table.put_item(Item=item)
    
    return Response(json.dumps(item), mimetype='application/json', status=200)

'''
@application.route('/tst/<temp>', methods=['GET'])
def tst_temp(temp):
    user_ip = str(request.environ['REMOTE_ADDR'])
    return (ip_meta(user_ip, temp))
'''
@application.route('/bi', methods=['GET'])
def get():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('eb_logger_log')
    # replace table scan
    resp = table.scan()
    print(str(resp))
    return Response(json.dumps(str(resp)), mimetype='application/json', status=200)

@application.route('/', methods=['GET'])
def post():
    # response = client.batch_get_item( RequestItems={ })
    # print(response)
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


def get_ip_meta():
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()

if __name__ == '__main__':
    flaskrun(application)
