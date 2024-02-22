#!/bin/bash

run_container () {
    tag=$1
    config=$2
    workers=$3

    echo "running container for config $config"
    # docker run -it -d -p 8080:8080 -e WORKERS=$workers --name $config $tag bash start-${config}.sh
    config=$config WORKERS=$workers docker compose up --wait
    sleep 1
}

run_locust () {
    users=$1
    result_prefix=$2
    user_class=$3

    echo "warming up"
    locust --config locust/locust.conf \
        --users 1 \
        --spawn-rate 1 \
        --run-time 2s \
        $user_class

    sleep 0.01

    echo "running locust test"
    locust --config locust/locust.conf \
        --users $users \
        --spawn-rate $users \
        --csv $result_prefix-$user_class \
        --capture-response-time 1 \
        $user_class
}

stop_container () {
    config=$1

    echo "stopping container for config $config"
    docker compose down
    # docker stop $config
    # docker rm $config
    echo ""
    sleep 2
}

users=5
workers=5

TAG=benchmark-target

RESULTS_DIR=results
mkdir -p $RESULTS_DIR

# set -e
# docker build -t $TAG -f Dockerfile app
# set +e

# config="gunicorn-sync-flask"
# run_container $TAG $config $workers
# run_locust $users $RESULTS_DIR/$config-sync SyncPassThroughUser
# stop_container $config

# exit 0

for user_class in "SyncPassThroughUser" "SyncCalcDistanceUser"
do
    for config in "gunicorn-sync-flask" "gunicorn-gevent-flask" "hypercorn-asyncio-quart" "hypercorn-uvloop-quart"
    do
        run_container $TAG $config $workers
        run_locust $users $RESULTS_DIR/$config-sync $user_class
        stop_container $config
    done
done

for user_class in "AsyncPassThroughUser" "AsyncCalcDistanceUser"
do
    for config in "hypercorn-asyncio-quart" "hypercorn-uvloop-quart"
    do
        run_container $TAG $config $workers
        run_locust $users $RESULTS_DIR/$config-async $user_class
        stop_container $config
    done
done

python aggregate_results.py
