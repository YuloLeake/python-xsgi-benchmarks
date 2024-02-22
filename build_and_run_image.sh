script=gunicorn-gevent-flask
# script=hypercorn-asyncio-quart

config=$script WORKERS=5 docker compose up --wait
echo "compose up"
sleep 5
echo "compose down"
docker compose down

# docker run -it -d -p 8080:8080 -e WORKERS=$workers --name $config $tag bash start-${config}.sh

# docker build -t benchmark-target -f Dockerfile app

# docker run -it -p 8080:8080 -e WORKERS=5 benchmark-target bash start-${script}.sh
