#!/bin/sh

gcloud config set project glossy-attic-237012
gcloud functions deploy parenttext-individualize-module-list \
--gen2 \
--region=europe-west2 \
--runtime=python311 \
--source=. \
--entry-point=serve \
--trigger-http
