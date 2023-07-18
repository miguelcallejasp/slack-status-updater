import functions_framework
from datetime import datetime, timedelta
import requests
import base64
import json


def epoch_time_in_amount_seconds(slack_status_duration_seconds: int):
    
    current_time = datetime.utcnow()
    print("Current time for the execution is: {}".format(current_time.strftime("%m/%d/%Y, %H:%M:%S")))
    future_time = current_time + timedelta(seconds=slack_status_duration_seconds)
    epoch_time = int(future_time.timestamp())
    print("The date when the status is going to be cleaned is (UTC): {} / {}".format(future_time.strftime("%m/%d/%Y, %H:%M:%S"), epoch_time))
    return epoch_time

def update_slack_status(slack_user: str,
                        slack_apikey: str,
                        slack_status_text: str,
                        slack_status_emoji: str,
                        slack_status_duration_seconds: int):
    
    expiration = epoch_time_in_amount_seconds(slack_status_duration_seconds)
    print("Status update for user {} and message: {}".format(slack_user, slack_status_text))
    
    built_headers = {
        "Content-type": "application/json; charset=utf-8",
        "Authorization": "Bearer {}".format(slack_apikey),
    }
    
    slack_url = "https://slack.com"
    slack_api_user_url = "/api/users.profile.set?user={}".format(slack_user)
    slack_api_payload = {
                            "profile": {
                                "status_text": "{}".format(slack_status_text),
                                "status_emoji": ":{}:".format(slack_status_emoji),
                                "status_expiration": int(expiration)
                            }
                        }
    print("Message being sent to Slack")
    print(json.dumps(slack_api_payload))
    try:
        r = requests.post(slack_url+slack_api_user_url, 
                          headers=built_headers,
                          data=json.dumps(slack_api_payload),
                          timeout=540)
        print(json.loads(r.content))
        print(r.status_code)
    except Exception as error:
        print(error)

@functions_framework.http
def main(request):

    # Example of payload from PubSub Scheduler:
    # This will be put in the payload request_json
    # {
    #     "slack_user": "pedro.perez",
    #     "slack_apikey": "xoxp-123456",
    #     "slack_status_text": "In class",
    #     "slack_status_emoji": "notebook",
    #     "slack_status_duration_seconds": 150 
    # }

    raw_data = request.data.decode('utf-8')
    raw_json = json.loads(raw_data)
    data_in_base64 = raw_json['data']['data']
    data_decoded = base64.b64decode(data_in_base64)
    request_json = json.loads(data_decoded.decode('utf-8'))
    
    update_slack_status(request_json['slack_user'],
                        request_json['slack_apikey'],
                        request_json['slack_status_text'],
                        request_json['slack_status_emoji'],
                        request_json['slack_status_duration_seconds'])

    return "Status update for {} was updated".format(request_json['slack_user'])
