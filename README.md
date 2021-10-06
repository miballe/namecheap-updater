# Namecheap Dynamic IP Updater
Python client to update Namecheap Dynamic DNS records

## Build Image
In the local folder run:

```
docker build -t namecheap-updateip .
```
This will create a new container image called `namecheap-updateip`. Remind to use `sudo` in case your deployment requires higher priviledges.

## Start Container Instance
The best option to start the container image is using `docker-compose`. This is file template.

```
version: "3.7"

services:
  nc-updater:
    image: namecheap-updateip
    container_name: ncupdater
    environment:
      - NAMECHEAP_DNS_PWD=8aae170c9b954acf8f6ee70aca2432a7,8f6ee70aca2432a78aae170c9b954acf
      - NAMECHEAP_DNS_HOST=@,host2
      - NAMECHEAP_DNS_RECORD=mydomain1.com,mydomain2.com
      - DETECT_IP=True
      - NEW_IP=0.0.0.0
      - UPDATE_INTEVAL_MINS=1
      - PYTHONUNBUFFERED=1
    restart: always
```