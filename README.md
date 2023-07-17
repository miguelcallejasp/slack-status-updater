# slack-status-updater
An overengineered Slack status updated. 

## Requirements
- A Slack token with `users.profile:write` permissions
- A Google Cloud Platform Service Account with the following permissions:
    - Google Cloud Storage
    - Google App Engine
    - Google Scheduler
    - Google Pub Sub 
