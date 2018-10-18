[![Build Status](https://travis-ci.org/ltalirz/aiida-qeq.svg?branch=master)](https://travis-ci.org/ltalirz/aiida-qeq) 
[![Coverage Status](https://coveralls.io/repos/github/ltalirz/aiida-qeq/badge.svg?branch=master)](https://coveralls.io/github/ltalirz/aiida-qeq?branch=master) 
[![Docs status](https://readthedocs.org/projects/aiida-qeq/badge)](http://aiida-qeq.readthedocs.io/) 
[![PyPI version](https://badge.fury.io/py/aiida-qeq.svg)](https://badge.fury.io/py/aiida-qeq)

# aiida-qeq

AiiDA plugin for computing electronic charges on atoms using equilibration-type models (QEq, EQEq, ...).

Templated using the [AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter).

## Installation

```shell
git clone https://github.com/ltalirz/aiida-qeq .
cd aiida-qeq
pip install -e .  # also installs aiida, if missing (but not postgres)
#pip install -e .[pre-commit,testing] # install extras for more features
verdi quicksetup  # better to set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit.py        # submit test calculation
verdi calculation list -a  # check status of calculation
```

If you have already set up your own aiida_qeq code using `verdi code setup`, you may want to try the following command:
```
qeq-submit  # uses aiida_qeq.cli
```

## Tests

The following will discover and run all unit test:
```shell
pip install -e .[testing]
python manage.py
```

## License

MIT


## Contact

leopold.talirz@gmail.com

