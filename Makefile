ifndef CONTAINER_ENGINE
CONTAINER_ENGINE = docker
endif

.PHONY: compose-up compose-down smoke-test compose-logs

compose-up:
	$(CONTAINER_ENGINE) compose up -d --build

compose-down:
	$(CONTAINER_ENGINE) compose down -v

compose-logs:
	$(CONTAINER_ENGINE) compose logs --tail=100 -f

smoke-test:
	./scripts/smoke_test.sh
