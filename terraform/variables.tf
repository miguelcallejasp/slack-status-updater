variable "gcp_project" {
  type        = string
}

variable "gcp_region_us_central1" {
  type        = string
  default     = "us-central1"
}

variable "gcp_zone_us_central1_c" {
  type        = string
  default     = "us_central1_c"
}

variable "storage_bucket_location" {
  type        = string
  default     = "slack-status-updater-code"
}