```shell script
docker run -it centos7/python3.6:v2 /bin/bash
#docker run -d -p 5050:5050 -v ./:/app -v ./keras:/root/.keras python:3.6
docker run -it -p 5050:5050 -v /home/wcy/segmentation:/app -v /home/wcy/segmentation/keras:/root/.keras python:3.6
```