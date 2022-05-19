terraform {
  backend "gcs" {
    bucket = "yatestap-tfstate"
    prefix = "cython"
  }
}
