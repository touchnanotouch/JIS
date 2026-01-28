.PHONY: help dev prod build up down logs clean \
        shell db-shell redis-shell migrate migrate-create \
        ps test restart


# Variables

COMPOSE_DEV = docker compose
COMPOSE_PROD = docker compose -f docker-compose.yml

# Commands

help:
	@echo "Docker Compose:"
	@echo "  make dev           - Build && up development services"
	@echo "  make prod          - Build && up production services"
	@echo "  make web-only      - Start web service"
	@echo "  make db-only       - Start db service"
	@echo "  make redis-only    - Start redis service"
	@echo "  make build         - Build images"
	@echo "  make up            - Create && start services"
	@echo "  make down          - Stop && remove services"
	@echo "  make start         - Start services"
	@echo "  make stop          - Stop services"
	@echo "  make logs          - Show logs"
	@echo "  make ps            - Show container status"
	@echo ""
	@echo "Container access:"
	@echo "  make shell         - Enter web container"
	@echo "  make db-shell      - Enter database"
	@echo "  make redis-shell   - Enter redis"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         - Remove everything"
	@echo "  make restart       - Restart services"

# Docker Compose

dev:
	$(COMPOSE_DEV) up --build -d

prod:
	$(COMPOSE_PROD) up --build -d

web-only:
	$(COMPOSE_DEV) up --no-deps -d web

db-only:
	$(COMPOSE_DEV) up --no-deps -d db

redis-only:
	$(COMPOSE_DEV) up --no-deps -d redis

build:
	$(COMPOSE_DEV) build

up:
	$(COMPOSE_DEV) up

down:
	$(COMPOSE_DEV) down

start:
	$(COMPOSE_DEV) start

stop:
	$(COMPOSE_DEV) stop

logs:
	$(COMPOSE_DEV) logs -f

ps:
	$(COMPOSE_DEV) ps

# Container access

shell:
	$(COMPOSE_DEV) exec web bash

db-shell:
	$(COMPOSE_DEV) exec db psql -U postgres

redis-shell:
	$(COMPOSE_DEV) exec redis redis-cli

# Maintenance

clean:
	$(COMPOSE_DEV) down -v --rmi all --remove-orphans

restart:
	$(COMPOSE_DEV) restart
