.PHONY: help
help:  ## Show available commands
	@echo "Available commands:"
	@echo
	@sed -n -E -e 's|^([A-Za-z0-9/_-]+):.+ ## (.+)|\1@\2|p' $(MAKEFILE_LIST) | column -s '@' -t

.PHONY: clean-pyc
clean-pyc:  ## Clean .pyc files
	find . -name \*.pyc -exec rm -f {} +
	find . -name \*.pyo -exec rm -f {} +
	find . -name \*~ -exec rm -f {} +
	find . -name __pycache__ -exec rmdir {} +

.PHONY: clean-build
clean-build:  ## Clean build files
	rm -rf build/
	rm -rf dist/
	rm -rf package/
	rm -rf __pycache__/
	rm -rf *.egg-info

clean: clean-pyc clean-build  ## Clean everything possible

.PHONY: build
build: clean-build  ## Build and package under package/python, using pip
	pip install --target ./package/python .

.PHONY: dist
dist: clean-build  ## Build dist packages for uploading to pypi
	python -m build

.PHONY: install
install:  ## Locally install with pip
	pip install --user .

.PHONY: upload
upload:  ## Upload to the PyPI package index
	python -m twine upload --repository pypi dist/*

.PHONY: upload-dev
upload-dev:  ## Upload to the TestPyPI package index (development)
	python -m twine upload --repository testpypi dist/*
