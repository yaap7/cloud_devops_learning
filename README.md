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

### Tests et constats

* Quand je push directement sur une branche : ??a lance le build.
* Quand je cr???? une pull request (PR) from `correct-something` to `dev`:
  * lors de la cr??ation de la PR, ??a ne relance pas un nouveau build puisque qu'il a d??j?? ??t?? fait sur cette branche avec ce commit lors du push pr??c??dent.
  * lors de l'acceptation (merge) de la PR, ??a lance le build sur la branche `dev`.
* Quand je cr???? une PR from `dev` to `prod`:
  * lors de la cr??ation de la PR, ??a **ne relance pas** un nouveau build. ??a utilise le build d'avant, probablement parce qu'il a r??ussi ?? d??tecter qu'il s'agissait de la m??me branche avec le m??me niveau de commit.
  * lors de l'acceptation (merge) de la PR, ??a lance un build sur la branche `prod`.

Les branches sont prot??g??es. On dirait que ??a n??cessite que le build sur la branche d'origine (par exemple, dev) soit valide avant de pouvoir pousser sur prod. Mais ??a ne v??rifie pas que le build sur prod fonctionne. ??a serait logique car le build a besoin que les changements soient appliqu??s pour pouvoir ??tre lanc??.
On ne peut pas non plus `git push --force` sur une branche prot??g??e.
On dirait que la bonne pratique est de pousser sur une autre branche, puis de cr??er des PR pour faire avancer les branches prot??g??es (dans notre exemple : dev et prod).
Mais comme je n'ai pas stock?? le tfstate dans Cloud Storage, je ne peux probablement pas supprimer les ressources !

### Ajout du tfstate dans Cloud Storage

On cr???? un nouveau bucket :

``` bash
PROJECT_ID=$(gcloud config get-value project)
gsutil mb gs://${PROJECT_ID}-tfstate
```

Optionnel : on active la gestion des versions des objets dans ce bucket :

``` bash
gsutil versioning set on gs://${PROJECT_ID}-tfstate
```

Pour ne pas que les versions reste ?? l'infini (et payer inutilement), on active une politique de suppression des anciennes versions (voir [cython/gs-lifecycle-config-file.json](cython/gs-lifecycle-config-file.json)) :

``` bash
gsutil lifecycle set cython/gs-lifecycle-config-file.json gs://${PROJECT_ID}-tfstate
```

On informe terraform qu'il doit stocker son tfstate dans ce bucket gr??ce au fichier [cython/backend.tf](cython/backend.tf).

Ensuite, j'ai pu pousser sur la branche `prod`, ce qui a d??ploy?? l'application dans GCP.
J'ai pu lancer `terraform init` pour initialiser le backend, et ainsi r??cup??rer l'??tat du provisionnement et voir que `terraform plan` ne proposait aucun changement car le push sur la branche avait d??j?? d??ploy?? les ressources.

Note : au d??but `terraform init` n'avait pas fonctionn??, donc j'avais du reconnecter mon compte via CLI gr??ce ?? la commande : `gcloud auth application-default login`.

### en cas de changement

Maintenant qu'on a une situation stable, il convient de v??rifier ce qu'il advient lorsqu'on modifie l'application et qu'on pousse son code.
Est-ce qu'une nouvelle "Compute Engine" est d??ploy??e ? avec une nouvelle adresse IP ? Est-ce que ??a remplace l'ancienne ? Est-ce que les r??gles de firewall sont supprim??es puis recr????es ?

No, it will not do anything because terraform just provision the ressource.
We should add an update mechanism in Cloud Build configuration.
Or, to try another service, I will play with App Engine to deploy the app automatically.
I will also use a git repo in Cloud Source Repositories, which will deploy on App Engine using Cloud Build.

See you there!

## Ressources

* <https://cloud.google.com/docs/terraform/get-started-with-terraform>
* <https://cloud.google.com/architecture/managing-infrastructure-as-code>
* <https://cloud.google.com/build/docs/automating-builds/build-repos-from-github>
* <https://cloud.google.com/docs/terraform/resource-management/store-state>
* <https://registry.terraform.io/providers/hashicorp/google/latest/docs>
