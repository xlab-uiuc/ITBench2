OCI_BIN = $(shell which docker || which podman)

IMG_REGISTRY ?= quay.io
IMG_NAMESPACE ?= it-bench
IMG = $(IMG_REGISTRY)/$(IMG_NAMESPACE)/k8s-topology-mapper:latest

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: build-image
build-image: ## Builds container image
	$(OCI_BIN) build -f Dockerfile -t $(IMG) --platform=linux/amd64

.PHONY: push-image
push-image: registry-login ## Pushes image to container registry
	$(OCI_BIN) push $(IMG)

.PHONY: build-push-image
build-push-image: build-image push-image ## Builds image and then pushes to registry
