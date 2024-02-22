#!/bin/bash

gunicorn -b 0.0.0.0:8080 -w ${WORKERS} -k gevent app_flask:app