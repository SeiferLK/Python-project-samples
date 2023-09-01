#!/bin/bash

network_name1="report_db_network"
#network_name1="cms_db_network"
network_name2="rev_proxy_network"

networks=($network_name1 $network_name2)
container_name="report_backend"


for network_name in "${networks[@]}"; do
    network_id=$(docker network ls | grep $network_name | awk '{print $1}')


    container_id=$(docker ps -a | grep $container_name | awk '{print $1}')

    echo "Attaching network $network_name ($network_id) to container $container_name ($container_id)"
    docker network connect $network_id $container_id
done
