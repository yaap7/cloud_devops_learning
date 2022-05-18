# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "cython-vm"
  machine_type = "f1-micro"
  project      = "yatestap"
  zone         = "europe-west1-c"
  tags         = ["ssh"]

  metadata = {
    enable-oslogin = "TRUE"
  }

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  # Install Flask
  metadata_startup_script = "sudo apt update; sudo apt install -yq build-essential python3 python3-pip rsync wget; pip install flask; wget -qO $HOME/app.py 'https://raw.githubusercontent.com/yaap7/cloud_devops_learning/main/cython/app.py'; nohup python3 $HOME/app.py &"

  network_interface {
    network = "default"

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}

resource "google_compute_firewall" "ssh" {
  name    = "allow-ssh"
  project = "yatestap"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = "default"
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "flask" {
  name    = "cython-app-firewall"
  project = "yatestap"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
}

// A variable for extracting the external IP address of the VM
output "Web-server-URL" {
 value = join("",["http://",google_compute_instance.default.network_interface.0.access_config.0.nat_ip,":5000"])
}
