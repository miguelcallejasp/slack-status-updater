import functions_framework
import datetime
import requests
import base64
import json



def update_slack_status(slack_user: str,
                        slack_apikey: str,
                        slack_status_text: str,
                        slack_status_emojix: str,
                        slack_status_duration_seconds: str):
    
    now = datetime.datetime.nowutc()
    print("Status update for user {} and message: {}".format(slack_user, slack_status_text))
    print("Expiration of the message will be at: {}".format(end_time))
    
    built_headers = {
        "Content-type": "application/json",
        "apikey": str(apikey),
        "tenant": str(tenant),
        "Keep-Alive": "timeout=540, max=10",
        "user-agent": "CloudFunctionsAnalytics/1.0.0"
    }
    
    try:
        r = requests.get(url+"/analytics/legacy/activitymonitor?timezone_string=America%2FNew_York&persist=True&daysBefore=1&reportHierarchyGroupCode="+tenant, headers=built_headers, timeout=540)
        #print(r)
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
