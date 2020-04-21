#!/bin/bash

export MODIN_ENGINE=Cloudburst
export MODIN_CONNECTION=127.0.0.1
export MODIN_IP=127.0.0.1

cd ../anna && ./scripts/start-anna-local.sh n 
cd ../cloudburst && ./scripts/start-cloudburst-local.sh n
cd ../modin

