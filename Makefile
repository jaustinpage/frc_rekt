.PHONY: deps_ubuntu
deps_ubuntu:
	sudo apt-get install python3 python3-pip python3-venv 

.PHONY: create_venv
create_venv:
	python -m venv ./env
	echo "Run `source ./env/bin/activate` each time you begin work`"
    
.PHONY: python_deps
python_deps:
	echo "Make sure you run `source ./env/bin/activate` before you run this command"
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

.PHONY: clean
clean:
	py3clean

.PHONY: pytest
pytest:
	pytest --color='yes' ./

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 ./   

.PHONY: init
init: deps_ubuntu create_venv python_deps download_curves

.PHONY: test
test: clean format pytest

