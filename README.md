frc_rekt - FRC Robot Electrical and Kinematic Tool
==================================================

[![CircleCI](https://circleci.com/gh/jaustinpage/frc_rekt.svg?style=shield&circle-token=ce65d30cde7772fda8b5a2f93fa28ff9efa42fb4)](https://circleci.com/gh/jaustinpage/frc_rekt)

This is a tool for modeling the electrical and kinematic properties of an 
FRC robot. It aims to make predictions about how a robot's electrical system
would respond to loads, in particular motors, and predict the effects of 
those loads.

This tool uses data from [motors.vex.com](http://motors.vex.com/).

Dependencies
------------

Depending on your os, you may have to install these yourself.

*  [Python 3.4+](https://www.python.org/downloads/)
*  [Pip](https://pypi.python.org/pypi/pip) (Note: should come with Python)
*  [Venv](https://docs.python.org/3/tutorial/venv.html) (Note: should also 
      come with Python)
*  [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html)
*  [motors.vex.com](http://motors.vex.com/) (Note: no need to download by 
      hand)

Setup
-----

1. Install the dependencies listed above, e.g. `
    make dependencies`
1. Create a virtual environment `
    python3 -m venv ./env  # Keeps your packages separate`
1. Activate the virtual environment `
    source env/bin/activate`
1. Install python dependencies `
    pip3 install --upgrade pip;
    pip3 install -r requirements.txt`
1. Download motor curve data from vex `
    cd vex_data/
    ./download_curves.py`

Running
-------

Until a proper package is created, this can be run manually. First, activate
the venv with `source env/bin/activate`. Then `./*.py` to run a module.

Developing
----------

Write good code. Before uploading, run `make prep` if you are on linux to 
prepare and run tests. Note: This will auto-format your files, so you probably
want to run this before you commit.

If pylint complains about misspelled words that are not misspelled, run
`make add_words_to_pylint` and the words that pylint is complaining about will
be added to the dictionary. Make sure you add the modified
.pylint_spelling_dict file to your commit, or you will not pass circleci.

Testing
-------

run `make prep` to run tests locally.

Other
-----

Find a bug? Algorithm doesn't work? Make an issue on github, and we will try to
fix it.
