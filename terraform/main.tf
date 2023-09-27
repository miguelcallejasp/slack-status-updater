data "google_secret_manager_secret_version" "slack_status_update_apikey" {
  project = var.gcp_project
  secret = "slack_status_update_apikey"
  version = "1"
}

data "google_secret_manager_secret_version" "slack_status_update_body" {
  project = var.gcp_project
  secret = "slack_status_update_body"
  version = "1"
}

# The local slack_apikey might not be used at all.
# I created it because I wanted to selectively add the apikey in the process.
# But the secret is being included in the slack_status_update_body entirely.
locals {
  slack_apikey = data.google_secret_manager_secret_version.slack_status_update_apikey.secret_data
  root_dir = abspath("${path.module}/src")
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = local.root_dir
  output_path = "${path.module}/slack_status_updater_code.zip"
}

resource "google_storage_bucket" "slack-status-function-bucket" {
  name          = "slack-status-function-bucket"
  location      = var.gcp_region_us_central1
  force_destroy = true  
  uniform_bucket_level_access = true
  storage_class = "STANDARD"
  versioning {
    enabled     = true
  }
}
resource "google_storage_bucket_object" "slack-status-function-code" {
  name   = "${data.archive_file.source.output_md5}.zip"
  bucket = "slack-status-function-bucket"
  source = data.archive_file.source.output_path
  depends_on = [google_storage_bucket.slack-status-function-bucket]
}

# The trigger
resource "google_pubsub_topic" "slack-status-update-trigger-topic" {
  name = "slack-status-update-trigger-topic"
  message_retention_duration = "342000s"
}

resource "google_cloudfunctions_function" "slack-status-function" {
  name        = "slack-status-function"
  description = "Slack Status Updater Cloud Function"
  runtime     = "python311"
  available_memory_mb   = 128
  source_archive_bucket = "${google_storage_bucket.slack-status-function-bucket.name}"
  source_archive_object = "${data.archive_file.source.output_md5}.zip"
  #trigger_http          = false
  timeout               = 540
  min_instances         = 0
  max_instances         = 100
  entry_point           = "main"
  region                = var.gcp_region_us_central1

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "${google_pubsub_topic.slack-status-update-trigger-topic.id}"
  }
  depends_on = [
    google_storage_bucket_object.slack-status-function-code,
    google_pubsub_topic.slack-status-update-trigger-topic
    ]
}

resource "google_cloud_scheduler_job" "slack-status-update-trigger-job" {
  name        = "slack-status-update-trigger-job"
  schedule    = "0 23 * * 1-4"

  pubsub_target {
     topic_name = "${google_pubsub_topic.slack-status-update-trigger-topic.id}"
     data       = base64encode(data.google_secret_manager_secret_version.slack_status_update_body.secret_data)
    }
}
