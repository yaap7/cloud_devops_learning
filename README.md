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

### python application

I created a first draft in [cython](cython/) directory.

It is a simple python web application which offers to encrypt and decrypt messages sent throught GET parameter.

### Provisionning using Terraform

The [main.tf](cython/main.tf) file provisions a "compute engine" in GCP with a dedicated VPC and firewall rules to open the port TCP 5000.
It is very similar to the one used in the [first tutorial](tf-tutorial/).

It automatically download the [cython app.py](cython/app.py) file and install flask to serve it on port TCP 5000.
It also show the URL to use to access the web application (especially the public IP).

It does not use Ansible to configure the deployed application.

### Automated deployment

This repository has been linked with "Cloud Build" from GCP to automatically deploy the `prod` branch on GCP using terraform.

It relies on the file [cloudbuild.yaml](cloudbuild.yaml) which describe the steps to launch when a push is made on any branch:

* `branch name`: simple action which display the branch name on which the push is made.
* `tf init`: goes into `cython` directory and run `terraform init`
* `tf plan`: goes into `cython` directory and run `terraform plan`
* `tf apply`: check if the current branch is `prod`, and launch `terraform apply --auto-approve`. Simply display the branch name otherwise.

## Ressources

* <https://cloud.google.com/docs/terraform/get-started-with-terraform>
* <https://cloud.google.com/architecture/managing-infrastructure-as-code>
* <https://cloud.google.com/build/docs/automating-builds/build-repos-from-github>
* <https://cloud.google.com/docs/terraform/resource-management/store-state>
* <https://registry.terraform.io/providers/hashicorp/google/latest/docs>
