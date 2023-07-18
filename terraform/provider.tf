terraform {
  required_version = "= 1.5.3"
  required_providers {
    google = "= 4.73.2"
  }
}
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region_us_central1
  zone    = var.gcp_zone_us_central1_c
  credentials = "${file("google_cloud_service_account.json")}"
}
