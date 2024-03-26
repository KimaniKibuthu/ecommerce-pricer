# Variables
REGISTRY_URL=kimani007
IMAGE_NAME=price-discovery
IMAGE_TAG=latest
CONTAINER_NAME=price-discovery-container

# Build the Docker image
build:
	docker build -t $(REGISTRY_URL)/$(IMAGE_NAME):$(IMAGE_TAG) .

# Push the Docker image to the registry
push:
	docker push $(REGISTRY_URL)/$(IMAGE_NAME):$(IMAGE_TAG)

# Pull the Docker image from the registry
pull:
	docker pull $(REGISTRY_URL)/$(IMAGE_NAME):$(IMAGE_TAG)

# Run the Docker container
run:
	docker run -p 8000:8000 -p 8501:8501 \
		--env-file .env \
		--name $(CONTAINER_NAME) \
		$(REGISTRY_URL)/$(IMAGE_NAME):$(IMAGE_TAG)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Remove the Docker image
clean:
	docker rmi $(REGISTRY_URL)/$(IMAGE_NAME):$(IMAGE_TAG)
