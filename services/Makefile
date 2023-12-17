THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timescale login-api db-shell
help:
	@echo "Makefile for the services"
	@echo "Usage:"
	@echo "    make build               Build the services"
	@echo "    make build-api           Build the api service"
	@echo "    make build-parser        Build the parser service"
	@echo "    make build-ml            Build the ml service"
	@echo "    make build-agent         Build the agent service"
	@echo "    make up                  Create and start containers"
	@echo "    make start               Start containers"
	@echo "    make down                Stop and remove containers, networks, images, and volumes"
	@echo "    make destroy             Stop and remove containers, networks, images, and volumes"
	@echo "    make stop                Stop services"
	@echo "    make restart             Restart services"
	@echo "    make logs                View output from containers"
	@echo "    make logs api            View output from api container"
	@echo "    make ps                  List containers"
	@echo "    make login-timescale     Login to timescale container"
	@echo "    make login-api           Login to api container"
	@echo "    make db-shell            Login to timescale container and open psql shell"
	@echo "    make help                Show this help message and exit"

rebuild_global:
	cd global_modules && ./rebuild_global_modules.sh

build:
	docker compose build
build-api:
	docker compose build api
build-parser:
	docker compose build parser_worker
build-ml:
	docker compose build ml_worker
build-agent:
	docker compose build agent_worker
build-storage:
	docker compose build vector_storage

up:
	docker compose up -d
start:
	docker compose start
down:
	docker compose down
destroy:
	docker compose down -v
stop:
	docker compose stop
restart:
	docker compose restart

logs:
	docker compose logs -f
ps:
	docker compose ps -a --services --filter "status=running"
