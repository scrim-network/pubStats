# pubstats

Creates a report of certain statistics regarding SCRiM publications on researchers.

_Minimum Python Version: 3.3_

## Install

### Using Make

```shell
make install
```

### Using pip

```shell
pip install .
```

*Note: it is not necessary to install pubstats to create the report.*

## Quick Start

### If pubstats is installed

If pubstats is installed, then it can be imported and run like any other Python module.

**Example**

```python
import pubstats

pubstats.display('key.csv', 'data.json', tags=None)
```

Another way to run pubstats is from the command line.

**Example**

```shell
pubstats-display
```

### Run from uninstalled repository

Use the ```-m``` flag when calling pubstats to run it directly from the repository's root folder without the need to install it.

**Example**

```shell
python -m pubstats
```

## Detailed Usage

### Common Parameters

Here are some common parameters found in most usage examples:

```key_file```: name of the authors key file (default is 'key.csv' located in the package's 'data' directory).

```data_file```: name of the publications data file (default is 'paperpile.json' located in the package's 'data' directory).

```tag_1 ... tag_n```: name of the tags used for data filtering. These are defined in ```data_file``` under 'labelsNamed'. All publications will be used unless tags are provided. Only publications with ```tag``` will be included in the report.

### Installed, saving report from the command-line

```shell
pubstats-save [key_file] [data_file] [tag_1 ... tag_n]
```

### Installed, display report to terminal from the command-line

```shell
pubstats-display [key_file] [data_file] [tag_1 ... tag_n]
```

### Installed, save from within Python

```python
import pubstats
pubstats.save(key_file='data/key.csv', data_file='data/paperpile.json', tags=None)
```

_```tags``` option must be a list._

### Installed, display from within Python

```python
import pubstats
pubstats.display(key_file='data/key.csv', data_file='data/paperpile.json', tags=None)
```

_```tags``` option must be a list._

### Uninstalled, display and save from the package directory

```shell
python -m pubstats [key_file] [data_file] [tag_1 ... tag_n]
```

## Other

When running the package without specified ```key_file``` or ```data_file```, faked data will be used as an example. Faked data were created with 'data_faker.py'. New faked data can be created by running this script with the ```--new``` option set:

```python
python data_faker.py --new
```

Running the script without the ```--new``` flag set will recreate the original data. _Package must be reinstalled when creating new faked data if running from the installed package. This does not apply when running it from the package directory using the ```-m``` flag._

## Data

This package uses 2 files: a CSV file with information about the authors, and a JSON file with information about the publications. The JSON file is exported directly from PaperPile. The first line of the CSV file should read like this:

```
first,last,role,institution,field,department,alias
```

Of these header columns, 'role', 'department', and 'alias' are optional. Alias can be used to identify an author with multiple spellings of their name. Simply create a row for each of these spellings but give them all the same name under 'alias'. (It could be anything, but make it unique to that author!)

An Excel spreadsheet can also be used in place of the CSV file. Make sure that the first sheet contains the relevant data.

The JSON file comes directly from PaperPile, but here is the basic structure if you'd like to create it manually:

```
[
  {
    "publisher": "Davis, Adams and Holland",
    "author": [
      {
        "last": "Wallace",
        "first": "Megan"
      },
      {
        "last": "Stanton",
        "first": "Edwin"
      },
      {
        "last": "Carroll",
        "first": "Alexis"
      },
      {
        "last": "Walker",
        "first": "Jacob"
      },
      {
        "last": "Randall",
        "first": "Gina"
      }
    ],
    "title": "Every simple that always hospital professor particularly.",
    "journal": "aggregate web-enabled e-commerce",
    "volume": "22",
    "pages": "275-314",
    "doi": "some.doi",
    "issue": "2",
    "labelsNamed": [
      "label3"
    ],
    "journalfull": "aggregate web-enabled e-commerce",
    "published": {
      "year": "1990"
    }
  }
]
```

## TODO

Currently, there is no way to tell the difference between 2 authors with the same name in the publications data. It would be nice to have an 'ID' field in the authors data, but PaperPile currently doesn't support that.
