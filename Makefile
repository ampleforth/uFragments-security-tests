.PHONY: ecr-login install build tag push pull

DOCKER_REPO ?= ufragments-security-tests
COMMIT_HASH = $(shell git rev-parse --short HEAD)
DOCKER_TAG ?= $(shell whoami)-$(COMMIT_HASH)
DOCKER_TAG_LATEST ?= 'latest'

AWS_ACCOUNT_ID ?= 834138259469
AWS_ECR_REGION ?= us-west-2
AWS_ECR_DOMAIN ?= $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com

ecr-login:
	@$(shell aws ecr get-login --no-include-email --region $(AWS_ECR_REGION))

build:
	@docker build -t $(DOCKER_REPO):$(DOCKER_TAG) .

tag:
	@docker tag $(DOCKER_REPO):$(DOCKER_TAG) $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG)
	@docker tag $(DOCKER_REPO):$(DOCKER_TAG) $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG_LATEST)
	
push: ecr-login tag
	@docker push $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG)
	@docker push $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG_LATEST)

pull: ecr-login
	@docker pull $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG_LATEST)

exec: pull
	@docker run -it $(AWS_ECR_DOMAIN)/$(DOCKER_REPO):$(DOCKER_TAG_LATEST) /bin/sh -c "./exec.sh"
