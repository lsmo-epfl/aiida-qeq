[![Build Status](https://travis-ci.org/ltalirz/aiida-qeq.svg?branch=master)](https://travis-ci.org/ltalirz/aiida-qeq)
[![Coverage Status](https://coveralls.io/repos/github/ltalirz/aiida-qeq/badge.svg?branch=master)](https://coveralls.io/github/ltalirz/aiida-qeq?branch=master)
[![Docs status](https://readthedocs.org/projects/aiida-qeq/badge)](http://aiida-qeq.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-qeq.svg)](https://badge.fury.io/py/aiida-qeq)

# aiida-qeq

AiiDA plugin for computing electronic charges on atoms using equilibration-type models (QEq, EQEq, ...).

Templated using the [AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter).

## Features

### QeQ charges
 * Add input structure in CIF format
  ```python
  CifData = DataFactory('cif')
  inputs['structure'] = CifData(file='/path/to/file')
  ```

 * Add parameters for electronegativity and Idempotential data of the elements.
  ```python
  SinglefileData = DataFactory('singlefile')
  inputs['parameters'] = SinglefileData(file='/path/to/file')
  ```

 * (optional) Specify `configure.input` options using a python dictionary and `QeqParameters`
  ```python
  QeqParameters = DataFactory('qeq.qeq')
  inputs['configure'] = QeqParameters(dict={'save_grid': [True, 'grid.cube']})
  ```

 * `QeqParameters` validates the command line options using [voluptuous](https://github.com/alecthomas/voluptuous).
  ```python
  QeqParameters = DataFactory('qeq.qeq')
  print(QeqParameters.schema)  # shows supported options
  ```

### EQeQ charges
 * Add input structure in CIF format
  ```python
  CifData = DataFactory('cif')
  inputs['structure'] = CifData(file='/path/to/file')
  ```

 * Add parameters for ionization data of the elements.
  ```python
  SinglefileData = DataFactory('singlefile')
  inputs['ionization_data'] = SinglefileData(file='/path/to/file')
  ```

 * Add parameters for common oxidation states of the elements.
  ```python
  SinglefileData = DataFactory('singlefile')
  inputs['charge_data'] = SinglefileData(file='/path/to/file')
  ```

 * Specify command line options using a python dictionary and `EQeqParameters`
  ```python
  EQeqParameters = DataFactory('qeq.eqeq')
  inputs['parameters'] = EQeqParameters(dict={'method': 'ewald'})
  ```

 * `EQeqParameters` validates the command line options using [voluptuous](https://github.com/alecthomas/voluptuous).
  ```python
  QeqParameters = DataFactory('qeq.eqeq')
  print(EQeqParameters.schema)  # show supported options
  ```

## Installation

```shell
pip install aiida-qeq
verdi quicksetup  # set up a new profile
verdi calculation plugins  # should now show your calclulation plugins
```

## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start         # make sure the daemon is running
cd examples
verdi run submit_qeq.py    # submit qeq test calculation
verdi run submit_eqeq.py   # submit eqeq test calculation
verdi process list -a  # check status of calculation
```

## Development

```shell
git clone https://github.com/ltalirz/aiida-qeq .
cd aiida-qeq
pip install -e .[pre-commit,testing]
pre-commit install  # enable pre-commit hooks
pytest              # run unit tests
```

## License

MIT


## Contact

leopold.talirz@gmail.com
