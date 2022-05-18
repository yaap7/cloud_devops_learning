# Learning of Terraform, Kubernetes and Google Cloud Platform

This is my notes taken during my learning of using Terraform, Kubernetes, and Google Cloud Platform (GCP).

The global steps are:

1. Create a small python application (e.g. to cypher and decypher text using an env var as key).
1. Deploy it using terraform and ansible (if needed).
1. Deploy it automatically using a "GitOps" way.
1. Deploy it more broadly using Google Kubernetes Engine (GKE).
1. See if the automated deployment could be made in GKE too.

## first tutorial to remember terraform usage

I followed [this tutorial](https://cloud.google.com/docs/terraform/get-started-with-terraform?hl=fr) to remember the terraform syntax.
The configuration is located in [tf-tutorial](./tf-tutorial).

I add to login using `gcloud auth application-default login` and to add a `project` attribute to all ressources.

Steps:

1. create the `main.tf` file
1. `terraform init` to intialize the directory with `.terraform` and plugins (such as the "google" provider)
1. `terraform plan` to plan the deployment.
1. `terraform apply` to apply the deployment.

The server works and reply to HTTP requests on port 5000.
It is available with a public IP shown after apply and with `terraform output`.

## application creation

I created a first draft in [cython](./cython) directory.

## Ressources

* <https://cloud.google.com/docs/terraform/get-started-with-terraform>
* <https://cloud.google.com/architecture/managing-infrastructure-as-code>
* <https://cloud.google.com/build/docs/automating-builds/build-repos-from-github>
* <https://cloud.google.com/docs/terraform/resource-management/store-state>
* <https://registry.terraform.io/providers/hashicorp/google/latest/docs>
