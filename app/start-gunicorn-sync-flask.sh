#!/bin/bash

gunicorn -b 0.0.0.0:8080 -w ${WORKERS} -k sync app_flask:app