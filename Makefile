SHELL := /usr/bin/env bash

INSTALL_SCRIPT = ./scripts/install.sh
ENV_SCRIPT = ./scripts/env.sh

.PHONY: help install deploy check-venv

help:
	@echo "Refer to the README file for detailed help."
	@echo
	@echo "Basic make commands:"
	@echo "    help"
	@echo "        Display this help message."
	@echo "    install"
	@echo "        Create virtual environment and install packages."
	@echo "    deploy"
	@echo "        Deploys the bot."

#===============
# Basic commands

install:
	@$(INSTALL_SCRIPT)

deploy: check-venv
	@echo "Deploying."
	@( \
		source $(ENV_SCRIPT) &>/dev/null; \
		cd $${SRC_PATH}; \
		(./$${DEPLOY_SCRIPT} &); \
	)
	@echo "Successfully deployed discord bot."

#==================
# Advanced commands

check-venv:
	@source $(ENV_SCRIPT) &>/dev/null || (echo "Env validation failed!  Check your installation!"; exit 1)

