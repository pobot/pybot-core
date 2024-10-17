SHELL = /bin/bash

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

define banner
	echo -e "\033[36m------------ $(1)...\033[0m"
endef

define progress
	echo -e "\033[34m... $(1)\033[0m"
endef

define success
	echo -e "\033[32m>>> $(1)\033[0m"
endef


.ONESHELL:

default: help

.PHONY: help
help: 				## show this help
	@echo -e "\n\033[37;1mAvailable targets:\033[0m\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' \
		| sort
	echo ""

.PHONY: dist
dist:				## build the package distribution wheel
	@$(call banner,"building distribution wheel")
	mkdir -p dist/arch
	mv dist/*.whl dist/arch 2> /dev/null || true
	python3 setup.py bdist_wheel


.PHONY: deploy
deploy:				## deploy the package on the target RPi
	@$(call banner,"deploying package on $(TARGET_HOST)")
	if [ "$$TARGET_HOST" = "" ] ; then echo "TARGET_HOST must be defined" ; exit 1 ; fi
	$(call progress,"uploading file...")
	scp dist/*.whl $(TARGET_HOST):
	$(call progress,"installing package...")
	ssh $(TARGET_HOST) -- pip3 install $$(cd dist ; ls *.whl) -U --user || exit 1
	$(call success,"Done")

.PHONY: clean
clean:				## clean the dist output directory
	@$(call banner,"cleaning build output artefacts")
	rm -f dist/*.whl wheel 
	rm -r build

.PHONY: init
init:				## installs the project dependencies
	@$(call banner,"installing project dependencies")
	pip install -U -r requirements-dev.txt
