IMAGE_NAME=telegram-bot
CONTAINER_NAME=telegram-bot
DOCKERFILE=./Dockerfile
BUILD_CONTEXT=.
TELEGRAM_BOT_TOKEN=""

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build           Build the Docker image."
	@echo "  run             Run the container in detached mode."
	@echo "  stop            Stop the running container."
	@echo "  remove          Remove the container."
	@echo "  logs            Show logs from the container."
	@echo "  clean           Remove the image and unused resources."
	@echo "  restart         Restart the container."

.PHONY: build
.PHONY: run
run:
	docker run -d --name telegram-bot -e TELEGRAM_BOT_TOKEN=$(TELEGRAM_BOT_TOKEN) $(IMAGE_NAME)

.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME)

.PHONY: remove
remove:
	docker rm $(CONTAINER_NAME)

.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: clean
clean:
	-docker rm $(CONTAINER_NAME) || true
	-docker rmi $(IMAGE_NAME) || true
	docker system prune -f

.PHONY: restart
restart: stop remove run
