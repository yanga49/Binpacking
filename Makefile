## install the software dependencies

SOURCES := $(shell find . -name '*.py')
TESTS := $(shell find . -name 'test_*.py')
MAIN_NOTEBOOK := report.ipynb

# Install software dependencies
install: 
	pipenv install --dev

# start a shell in the virtual environment
shell:
	pipenv shell

# Start Jupyter server and open the main notebook
jupyter:
	pipenv run python -m jupyter lab $(MAIN_NOTEBOOK)

# Run flake8 on top of the source files
lint:
	pipenv run python -m flake8 $(SOURCES)

# Run tests and compute coverage infos
test:
	pipenv run python -m coverage run -m pytest -v $(TESTS)
	pipenv run python -m coverage report 

benchmark:
	pipenv run python sample_bench.py -o sample_bench.json

uml: uml/initial.pdf
uml/initial.pdf: uml/initial.puml
	plantuml -tsvg uml/initial.puml
	rsvg-convert -f pdf -o uml/initial.pdf uml/initial.svg
	rm -f uml/initial.svg

# clean temporary files
clean:
	rm -rf .vscode
	rm -rf uml/*.pdf
	rm -rf .pytest_cache .vscode __pycache__ .coverage
	rm -rf .ipynb_checkpoints macpacking/.ipynb_checkpoints
	rm -rf macpacking/__pycache__ macpacking/algorithms/__pycache__

# Delete the virtual environment for this project
clobber:
	pipenv --rm

