#!/bin/bash

hypercorn -b 0.0.0.0:8080 -w ${WORKERS} -k uvloop app_quart:app