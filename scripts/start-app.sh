#!/bin/bash

cd back
sudo systemctl start docker
sudo docker rm app
sudo docker run -d --name app -p 8000:8000 app
