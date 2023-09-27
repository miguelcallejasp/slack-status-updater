# Slack Status Updater
An overengineered Slack Status updater. 

## Requirements
- A Slack token with `users.profile:write` permissions
- A Google Cloud Platform Service Account with the following permissions:
    - Google Cloud Storage
    - Google App Engine
    - Google Scheduler
    - Google Pub Sub
    - Google Secret Manager

## Setup
Create the following Secrets in Google Secret Manager

- `slack_status_update_body` with the following value:
```json
{
  "slack_user": "your.slack.user",
  "slack_apikey": "xoxp-your-slack-api-key",
  "slack_status_text": "The text of your status",
  "slack_status_emoji": ":balloon:",
  "slack_status_duration_seconds": 9000
}
```

Where the `slack_status_emoji` is the short version of the emoji in the format `:notebook:` without the semicolons. And the `slack_status_duration_seconds` is how long
the status will be available in seconds. 

- `slack_status_update_apikey` with the value of the Slack API Key. I think I'm not using this anymore, although I would need to review it. 

### Destroy
Just hit `terraform destroy` and everything will be gone. 