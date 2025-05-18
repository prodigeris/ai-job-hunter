.PHONY: env activate

# Python virtual environment name
VENV_NAME = venv

env:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_NAME)
	@echo "To activate the environment, run: make activate"

activate:
	@echo "Activating virtual environment..."
	@exec /bin/zsh -c "source $(VENV_NAME)/bin/activate && exec /bin/zsh"

help:
	@echo "Available commands:"
	@echo "  make env      - Create virtual environment"
	@echo "  make activate - Activate virtual environment" 