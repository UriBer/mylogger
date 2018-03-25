import requests
import boto3
import datetime
from flask import Response
import json

def ip_meta(ip, path):
    service_url = 'http://freegeoip.net/json/{}'.format(ip) 
    response = requests.get(service_url).json()
    #dynamodb = boto3.resource('dynamodb')
    #table = dynamodb.Table('eb_logger_log')
    res_data = {k: v for k, v in response.items() if v!=''}
    print(res_data)
    '''
    table.put_item(
    Item={
        'path': path,
        'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ip_meta' : res_data
         }
    )
    '''
    #         'ip meta': {k: v for k, v in response.items() if v is not None},

    #return render_template('index.html', title='Stats', response=response) 
    return Response(json.dumps({'{}'.format(str(path)) : '{}'.format(res_data)}), mimetype='application/json', status=200)
'''
if __name__ == '__main__':
    ip_meta('127.0.0.1', 'tst')
'''