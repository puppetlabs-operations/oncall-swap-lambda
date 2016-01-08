from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from datetime import time

import json
import requests

print('Loading function')


def lambda_handler(event, context):
    with open('./config.json') as f:
        config = json.loads(f.read())
    print("Received event: " + json.dumps(event, indent=2))
    s = requests.Session()
    s.headers.update({'Authorization': 'Token token={key}'.format(key=config['pd_api_key'])})
    current_date = datetime.today()
    schedule_params = {
        'since': datetime.isoformat(datetime.combine(current_date, time(0))),
        'until': datetime.isoformat(datetime.combine(current_date, time(0, 5))),
    }
    r = s.get(config['pd_url'] + '/api/v1/schedules/{sched_id}/users'.format(sched_id=config['pd_secondary_schedule']), params=schedule_params)
    oncall_user = r.json()
    print("Oncall User:\n" + str(oncall_user))
    paged = False
    conecutive_pages = 0
    for i in range(config['consecutive_days_paged']):
        oncall_date = current_date - timedelta(days=i)
        incident_params = {
            'status': 'triggered',
            'service': config['pd_service'],
            'since': datetime.isoformat(datetime.combine(oncall_date, time(config['pd_swap_range']['start']))),
            'until': datetime.isoformat(datetime.combine(oncall_date, time(config['pd_swap_range']['end']))),
        }
        print("Incident Params:\n" + str(incident_params))
        r = s.get(config['pd_url'] + '/api/v1/incidents/count', params=incident_params)
        incident_count = r.json()
        print(incident_count)
        print("Incident Count:\n" + str(incident_count['total']))
        if incident_count['total'] > 0:
            if paged:
                conecutive_pages += 1
            paged = True
        else:
            if not paged:
                consecutive_pages = 0
            paged = False
        if consecutive_pages  >= config['consecutive_days_paged']:
            override_data = {
                'override': {
                    'user_id': oncall_user['users'][0]['id'],
                    'start': datetime.isoformat(datetime.combine(current_date, time(5, 5))),
                    'end': datetime.isoformat(datetime.combine(current_date + timedelta(days=1), time(6))),
                }
            }
            print("Override Data:\n" + str(override_data))
            r = s.post(config['pd_url'] + '/api/v1/schedules/{sched_id}/overrides'.format(sched_id=config['pd_primary_schedule']), json=override_data)
            print(r.text)
            break
