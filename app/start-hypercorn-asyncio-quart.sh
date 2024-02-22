#!/bin/bash

hypercorn -b 0.0.0.0:8080 -w ${WORKERS} -k asyncio app_quart:app