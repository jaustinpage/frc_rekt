.PHONY: dependencies
dependencies:
	scripts/dependencies

.PHONY: prep
prep: 
	scripts/prep

.PHONY: test
test:
	scripts/test

.PHONY: update_branch
update_branch:
	git pull --rebase origin master

.PHONY: add_words_to_pylint
add_words_to_pylint:
	env/bin/pylint --rcfile=setup.cfg --spelling-store-unknown-words=yes --reports=n ./frc_rekt/ ./tests/
