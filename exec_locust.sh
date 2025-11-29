#!/bin/bash
USERS=50
SPAWN_RATE=10
RUN_TIME="5m"
LOCUST_FILE="locustfile.py"
CSV_PREFIX="resultados"

locust -f "$LOCUST_FILE" \
  --users "$USERS" \
  --spawn-rate "$SPAWN_RATE" \
  --run-time "$RUN_TIME" \
  --csv "$CSV_PREFIX"