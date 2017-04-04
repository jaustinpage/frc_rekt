.PHONY: deps_ubuntu
deps_ubuntu:
	sudo apt-get install python3 python3-pip python3-venv python3-pandas

.PHONY: create_venv
create_venv:
	python3 -m venv --clear ./env
	echo "Run \`source ./env/bin/activate\` each time you begin work"
    
.PHONY: python_deps
python_deps:
	echo "Run \`source ./env/bin/activate\`"
	echo "Run \`python3 -m pip install --upgrade pip\`"
	echo "Run \`python3 -m pip install -r requirements.txt\`"

.PHONY: download_curves
download_curves:
	cd data/vex; ./download_curves.py; cd -

.PHONY: init
init: deps_ubuntu create_venv

.PHONY: clean
clean:
	py3clean ./frc_rekt/

.PHONY: format
format:
	yapf --in-place --recursive --style pep8 ./frc_rekt/

.PHONY: lint
lint:
	pylint ./frc_rekt/

.PHONY: codestyle
codestyle:
	pycodestyle ./frc_rekt
	pydocstyle ./frc_rekt

.PHONY: check_format
check_format:
	if [ -z "`yapf --recursive --style pep8 --diff ./frc_rekt/`" ]; then exit 0; else exit 1; fi

.PHONY: pytest
pytest:
	pytest --color='yes' ./frc_rekt/

.PHONY: prep
prep: format lint codestyle pytest clean

.PHONY: test
test: check_format lint pytest

.PHONY: update_branch
update_branch:
	git pull --rebase origin master

.PHONY: add_words_to_pylint
add_words_to_pylint:
	pylint --spelling-store-unknown-words=yes ./frc_rekt/
