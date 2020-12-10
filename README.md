[![Build Status](https://github.com/lsmo-epfl/aiida-qeq/workflows/ci/badge.svg)](https://github.com/lsmo-epfl/aiida-qeq/actions)
[![Coverage Status](https://codecov.io/gh/lsmo-epfl/aiida-qeq/branch/develop/graph/badge.svg)](https://codecov.io/gh/lsmo-epfl/aiida-qeq)
[![Docs status](https://readthedocs.org/projects/aiida-qeq/badge)](http://aiida-qeq.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-qeq.svg)](https://badge.fury.io/py/aiida-qeq)

# aiida-qeq

AiiDA plugin for computing electronic charges on atoms using equilibration-type models using the [Qeq method](https://github.com/danieleongari/egulp) and the [EQeq method](https://github.com/danieleongari/eqeq).

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

In order to work, the commands `egulp` (for Qeq) and `eqeq` (for EQeq) needs to work on the machine and run the code's exectuable.
To get these programs you can look into [danieleongari/egulp](https://github.com/danieleongari/egulp)
and [danieleongari/EQeq](https://github.com/danieleongari/EQeq)
or the compiled binaries provided within [lsmo-epfl/aiida-lsmo-codes](https://github.com/lsmo-epfl/aiida-lsmo-codes).

A quick demo of how to submit a calculation:
```shell
cd examples
verdi run run_qeq.py    # submit qeq test calculation
verdi run run_eqeq.py   # submit eqeq test calculation
verdi process list -a  # check status of calculation
```

## Development

```shell
git clone https://github.com/lsmo-epfl/aiida-qeq
cd aiida-qeq
pip install -e .['pre-commit','testing']
pytest
```

If you are changing the inputs of existing tests or need to regenerate test data, place an `.aiida-testing-config.yml`
file in your repository that points to the required simulation codes:
```yaml
---
mock_code:
  # code-label: absolute path
  egulp-fc4d7b7: /path/to/cp2k.sopt
  eqeq-6490320: /path/to/Chargemol_09_02_2017_linux_serial
```

## License

MIT


## Contact

leopold.talirz@gmail.com
