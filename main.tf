/*
TODO: Integration with Terraform

provider "google" {
  credentials = file("chocobot-413408-2b455b9c8e8b.json.json")
  project     = "chocobot-413408"
  region      = "us-central1"
  zone        = "us-central1-a"
}

resource "google_compute_instance" "instance-1" {
  name         = "instance-1"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP
    }
  }

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }

  scheduling {
    preemptible       = false
    on_host_maintenance = "MIGRATE"
    automatic_restart = true
  }
}
*/