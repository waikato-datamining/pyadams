# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# jvm.py
# Copyright (C) 2024 Fracpete (fracpete at waikato dot ac dot nz)

import logging
import os
from typing import List

import pyadams.core.platform as platform
import jpype
from jpype import JClass
from wai.logging import init_logging


ENV_PYADAMS_LOGLEVEL = "PYADAMS_LOGLEVEL"
""" environment variable for the global default logging level. """

is_started = None
""" whether the JVM has been started """

is_headless = None
""" whether we are running in headless mode. """

# logging setup
init_logging(env_var=ENV_PYADAMS_LOGLEVEL)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


def add_lib_dir(root_dir: str, cp: List[str]):
    """
    Adds the ADAMS library dirs to the classpath.

    :param root_dir: the ADAMS root directory to use
    :type root_dir: str
    :param cp: the list to append the classpath to
    :type cp: list
    """
    if not os.path.exists(root_dir):
        raise Exception("ADAMS root dir does not exist: %s" % root_dir)

    cp.append(os.path.join(root_dir, "lib", "*"))

    sub_dir = None
    if platform.is_linux():
        sub_dir = "linux64"
    elif platform.is_windows():
        sub_dir = "windows64"
    elif platform.is_mac():
        sub_dir = "macosx64"
    if sub_dir is not None:
        cp.append(os.path.join(root_dir, "lib", sub_dir, "*"))


def add_system_classpath(cp: List[str]):
    """
    Adds the system's classpath to the JVM's classpath.

    :param cp: the list to append the classpath to
    :type cp: list
    """
    if 'CLASSPATH' in os.environ:
        parts = os.environ['CLASSPATH'].split(os.pathsep)
        for part in parts:
            cp.append(part)
    else:
        _logger.warning("Cannot add system's classpath, as environment variable CLASSPATH not set.")


def start(root_dir: str, system_cp: bool = False, max_heap_size: str = None, headless: bool = False,
          system_info=False, convert_strings: bool = True, logging_level: int = logging.DEBUG):
    """
    Initializes the jpype connection (starts up the JVM).

    :param root_dir: the ADAMS root directory (above the lib/bin dirs)
    :type root_dir: str
    :param system_cp: whether to add the system classpath as well
    :type system_cp: bool
    :param max_heap_size: the maximum heap size (-Xmx parameter, eg 512m or 4g)
    :type max_heap_size: str
    :param headless: whether to run in headless mode
    :type headless: bool
    :param system_info: whether to print the system info (generated by adams.core.SystemInfo)
    :type system_info: bool
    :param convert_strings: whether to convert strings automatically between Java and Python
    :type convert_strings: bool
    :param logging_level: the logging level to use for this module, e.g., logging.DEBUG or logging.INFO
    :type logging_level: int
    """
    global is_started, is_headless, _logger

    _logger.setLevel(logging_level)

    if is_started is not None:
        _logger.info("JVM already running, call jvm.stop() first")
        return

    full_cp = []

    add_lib_dir(root_dir, full_cp)

    # TODO custom WEKA_HOME env var?
    # heuristic: pick latest weka sub-dir
    # $HOME/.adams/wekafiles/X.Y.Z

    if system_cp:
        _logger.debug("Adding system classpath")
        add_system_classpath(full_cp)

    _logger.debug("Classpath=" + str(full_cp))

    args = []

    # heapsize
    if max_heap_size is not None:
        _logger.debug("MaxHeapSize=%s" % max_heap_size)
        args.append("-Xmx%s" % max_heap_size)
    else:
        _logger.debug("MaxHeapSize=default")

    # headless mode
    is_headless = headless
    if headless:
        args.append("-Djava.awt.headless=true")

    jpype.startJVM(*args, classpath=full_cp, convertStrings=convert_strings)
    is_started = True

    if system_info:
        _logger.debug(JClass("adams.core.SystemInfo")())


def stop():
    """
    Kills the JVM.
    """
    global is_started
    if is_started is not None:
        is_started = None
        jpype.shutdownJVM()
