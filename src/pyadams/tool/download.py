import argparse
import json
import logging
import os
import requests
import traceback
import zipfile
from typing import Dict, Optional

from wai.logging import init_logging, set_logging_level, add_logging_level
from pyadams.core.jvm import ENV_PYADAMS_LOGLEVEL
from pyadams.core.project import init_project_dir, project_dir

DOWNLOAD = "pa-download"

_logger = logging.getLogger(DOWNLOAD)

ACTION_UPDATE = "update"
ACTION_LIST = "list"
ACTION_DOWNLOAD = "download"
ACTIONS = [
    ACTION_UPDATE,
    ACTION_LIST,
    ACTION_DOWNLOAD,
]

DOWNLOADS_URL = "https://raw.githubusercontent.com/waikato-datamining/pyadams/main/downloads.json"


def _downloads_info_file() -> str:
    """
    Returns the filename for the local downloads information.

    :return: the filename
    :rtype: str
    """
    return os.path.join(project_dir(), "downloads.json")


def update_downloads_info():
    """
    Updates the download information.
    """
    init_project_dir()
    _logger.info("Retrieving: %s" % DOWNLOADS_URL)
    r = requests.get(DOWNLOADS_URL)
    if r.status_code == 200:
        _logger.info("Writing downloads info to: %s" % _downloads_info_file())
        with open(_downloads_info_file(), "w") as fp:
            fp.write(r.text)
    else:
        _logger.error("Failed to download: code=%d" % r.status_code)


def _load_downloads() -> Optional[Dict]:
    """
    Loads the downloads info file and returns the dictionary. Updates it if missing.

    :return: the download info, None if failed to load
    :rtype: dict
    """
    init_project_dir()
    if not os.path.exists(_downloads_info_file()):
        _logger.warning("No downloads information available, attempting update...")
        update_downloads_info()
    if not os.path.exists(_downloads_info_file()):
        _logger.error("No downloads information available (%s), cannot load information!" % _downloads_info_file())
        return None
    with open(_downloads_info_file(), "r") as fp:
        return json.load(fp)


def list_downloads():
    """
    Lists all available downloads.
    """
    info = _load_downloads()
    if info is None:
        _logger.error("No downloads information available (%s), cannot list information!" % _downloads_info_file())
        return
    print("version/name")
    for version in info:
        for name in info[version]:
            print("%s/%s" % (version, name))


def download(version: str, name: str, output_dir: str, extract: bool):
    """
    Downloads the specified version.

    :param version: the version, e.g., snapshot
    :type version: str
    :param name: the name of the download, e.g., adams-ml-app
    :type name: str
    :param output_dir: the directory to download to
    :type output_dir: str
    :param extract: whether to extract the archive as well
    :type extract: bool
    """
    info = _load_downloads()
    if info is None:
        _logger.error("No downloads information available (%s), cannot perform download!" % _downloads_info_file())
        return
    if version not in info:
        _logger.error("Version '%s' not available!" % version)
        list_downloads()
        return
    if name not in info[version]:
        _logger.error("Name '%s' not available for version '%s'!" % (name, version))
        list_downloads()
        return

    # download
    url = info[version][name]
    _logger.info("Downloading: %s" % url)
    local_filename = os.path.join(output_dir, url.split('/')[-1])
    _logger.info("Local file: %s" % local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # extract?
    if extract:
        _logger.info("Extracting '%s' to: %s" % (local_filename, output_dir))
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(output_dir)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_PYADAMS_LOGLEVEL)
    parser = argparse.ArgumentParser(
        description="Tool for downloading ADAMS releases and snapshots.",
        prog=DOWNLOAD,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--action", choices=ACTIONS, help="The action to perform.", default=None, type=str, required=True)
    parser.add_argument("-v", "--version", help="The version to download, e.g., 'snapshot'.", default=None, type=str, required=False)
    parser.add_argument("-n", "--name", help="The name of the download, e.g., 'adams-ml-app'.", default=None, type=str, required=False)
    parser.add_argument("-o", "--output_dir", help="The directory to download ADAMS to.", default=None, type=str, required=False)
    parser.add_argument("-x", "--extract", action="store_true", help="Whether to automatically extract the downloaded ADAMS archive.", required=False)
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    if parsed.action == ACTION_UPDATE:
        update_downloads_info()
    elif parsed.action == ACTION_LIST:
        list_downloads()
    elif parsed.action == ACTION_DOWNLOAD:
        download(parsed.version, parsed.name, parsed.output_dir, parsed.extract)
    else:
        raise Exception("Unknown action: %s" % parsed.action)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    main()
