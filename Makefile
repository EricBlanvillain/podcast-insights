PYTHON = python3
PIP = $(PYTHON) -m pip

.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev:
	$(PIP) install -r requirements-dev.txt

.PHONY: test
test:
	pytest tests/ -v

.PHONY: lint
lint:
	flake8 src tests
	isort src tests
	black src tests

.PHONY: run
run:
	streamlit run src/app.py

.PHONY: docker-build
docker-build:
	docker-compose build

.PHONY: docker-run
docker-run:
	docker-compose up

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete