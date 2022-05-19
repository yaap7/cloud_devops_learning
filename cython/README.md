# cython

This is the demo application to play with deployments.

## app.py

This is the main file for the python application.
It is called cython as a reduction of crypt-python.

I simply offers two endpoints:

* `/encrypt?text=<plain_text_to_crypt>`
* `/decrypt?text=<encrypted_text_to_decrypt>`

It uses a very simple "crypt" method for now: `base64` encoding.

## main.tf

It is used by terraform to deploy the application on a "compute engine" in GCP.
