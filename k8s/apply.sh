#!/bin/bash

export NS=

if [ "${NS}" == "" ]; then
  echo "Set the NS environment variable to your desired namespace"
  exit
fi

kubectl -n ${NS} apply -f datavolumes.yaml
kubectl -n ${NS} apply -f config.yaml
kubectl -n ${NS} apply -f database.yaml
kubectl -n ${NS} apply -f avg.yaml
kubectl -n ${NS} apply -f ingress.yaml