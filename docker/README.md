# Docker containers

## 0-singularity-base

The `0-singularity-base` container is based on an nvidia cuda base image and has `pytorch` and other large slow to compile libraries pre-built.

## llm-service

This container exposes a simple webservice that allows remote agents access to generative models. 

## llm-webapp

This container is a `node.js` frontend which communicates with the `llm-service` container

## model-manager

This container is meant maintain a local copy of various models in a well known directory.  It can be run manually when a particular model needs tob e downloaded or in an automated way so that it keeps existing models up to date.  While it's main goal is to monitor configured huggingface models, it will eventually be able to pull models from other sources.

## model-tuner

This container is all about taking a model and a dataset and producing a new model. 

