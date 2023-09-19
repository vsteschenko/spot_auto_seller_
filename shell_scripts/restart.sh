#!/usr/bin/env bash

container_name="spot_auto_seller"
image_location="ghcr.io/arcadiyyyyyyyy/spot_auto_seller/spot_auto_seller:refs_heads_prod"

echo "Started stopping the container"

docker stop $container_name
docker rm $container_name
docker pull $image_location
docker run --name=$container_name -d --env-file=prod.env --network=host $image_location
docker rmi -f "$(docker images -aq -f "dangling=true")"

echo "Restarted!"
