# pyadams
Python library for using [ADAMS](https://adams.cms.waikato.ac.nz/) from Python (via JPype).


## Installation

From PyPI:

```bash
pip install pyadams
```

Or directly from Github:

```bash
pip install git+https://github.com/waikato-datamining/pyadams.git
```


## Tools

### Download

```
usage: pa-download [-h] -a {update,list,download} [-v VERSION] [-n NAME]
                   [-o OUTPUT_DIR] [-x]
                   [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for downloading ADAMS releases and snapshots.

optional arguments:
  -h, --help            show this help message and exit
  -a {update,list,download}, --action {update,list,download}
                        The action to perform. (default: None)
  -v VERSION, --version VERSION
                        The version to download, e.g., 'snapshot'. (default:
                        None)
  -n NAME, --name NAME  The name of the download, e.g., 'adams-ml-app'.
                        (default: None)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to download ADAMS to. (default: None)
  -x, --extract         Whether to automatically extract the downloaded ADAMS
                        archive. (default: False)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```
