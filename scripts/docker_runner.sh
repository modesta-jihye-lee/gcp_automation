HOST_PATH=/gcp_automation
CONTAINER_NAME=gcp_automation

docker run -it --rm -v $HOST_PATH:/app --network host --name $CONTAINER_NAME gcp-vm-automation:latest bash