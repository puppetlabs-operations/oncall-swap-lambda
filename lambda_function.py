from __future__ import print_function

import json
import requests

print('Loading function')


def lambda_handler(event, context):
    with open('./config.json') as f:
        config = json.loads(f.read())
    print("Received event: " + json.dumps(event, indent=2))
    s = requests.Session()
    s.headers.update({'Authorization': 'Token token={key}'.format(key=config['pagerduty_api_key'])})
