#!/bin/bash

cd ../anna && ./scripts/stop-anna-local.sh pids
cd ../cloudburst && ./scripts/stop-cloudburst-local.sh pids && cd ../modin

