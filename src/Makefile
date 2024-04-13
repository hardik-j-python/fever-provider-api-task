# Makefile

# Define the Python interpreter to use
PYTHON = python3

# Define the Django management command to run the server
MANAGE_CMD = manage.py

# Define the port to run the server on
PORT = 8000

# Create virtual environment
create-virtualenv:
	@echo Creating virtual environment.
	virtualenv venv

# Activate the virtual environment
activate-env:
	@echo Activating virtual environment.
	. venv/bin/activate

# Target to install Python dependencies
install-dependencies:
	@echo Installing dependencies of the project.
	$(PYTHON) -m pip install -r ../requirements.txt

# Target to run Django database migrations
migrate:
	@echo migrating the changes to Database.
	$(PYTHON) $(MANAGE_CMD) migrate

# Run the custom manage py command to load the data in the database
load-data:
	@echo Fetching data from the provider and storing it in the database.
	$(PYTHON) $(MANAGE_CMD) sync_external_provider

# Target to run the Django development server
run:
	@echo Running development server at 8000 PORT.
	$(PYTHON) $(MANAGE_CMD) runserver $(PORT)

# To run the project first time in your machine.
first-time: create-virtualenv activate-env install-dependencies migrate load-data run
	@echo Process completed successfully.
