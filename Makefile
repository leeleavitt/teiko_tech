# Detect the operating system (Linux, OSX, etc)
OS := $(shell uname)

# URL for the Mambaforge installer
MAMBA_URL_LINUX=https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
MAMBA_URL_OSX=https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-x86_64.sh

# Choose the installer based on the operating system
ifeq ($(OS),Linux)
	MAMBA_URL=$(MAMBA_URL_LINUX)
endif
ifeq ($(OS),Darwin)
	MAMBA_URL=$(MAMBA_URL_OSX)
endif

# Target to install mambaforge
.PHONY: install-mambaforge
install-mambaforge:
	@echo "Checking if mamba is installed..."
	@command -v mamba > /dev/null 2>&1 || (echo "Mamba is not installed. Installing Mambaforge..."; \
	curl -o Mambaforge.sh -L $(MAMBA_URL) && \
	bash Mambaforge.sh -b -p "${HOME}/conda" && \
	bash "${HOME}/conda/etc/profile.d/conda.sh" && \
	bash $(HOME)/conda/bin/conda init && \
	rm Mambaforge.sh; \
	echo "Mambaforge installation complete.")

# Target to create dev env with poetry and python 3.10
.PHONY: create-dev-env
create-dev-venv:
	@echo "creating dev env at .dev-venv"
	$(HOME)/conda/bin/mamba create -c conda-forge -p .dev-venv -y python=3.10 conda-lock

# Target to lock dependencies using conda-lock
.PHONY: lock
lock:
	@echo "locking dependencies"
	.dev-venv/bin/conda-lock lock --no-mamba -f pyproject.toml

# Target to install venv from lock file using conda-lock
.PHONY: venv
venv:
	@echo "installing venv from lock file"
	.dev-venv/bin/conda-lock install -p .venv conda-lock.yml