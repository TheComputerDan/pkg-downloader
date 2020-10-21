#!/bin/bash

# Install dependancies, gnupg was added since it isn't in the base image.
apt install -y apt-transport-https ca-certificates wget gnupg
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
sh -c 'echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" > /etc/apt/sources.list.d/elastic-7.x.list'
apt update -y