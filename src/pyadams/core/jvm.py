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
import sys
from typing import List

import jpype

started = None
""" whether the JVM has been started """

# logging setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    if sys.platform == "linux":
        sub_dir = "linux64"
    elif sys.platform == "win32":
        sub_dir = "windows64"
    elif sys.platform == "darwin":
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
        logger.warning("Cannot add system's classpath, as environment variable CLASSPATH not set.")


def start(root_dir: str, system_cp: bool = False, max_heap_size: str = None, headless: bool = False,
          convert_strings: bool = True, logging_level: int = logging.DEBUG):
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
    :param convert_strings: whether to convert strings automatically between Java and Python
    :type convert_strings: bool
    :param logging_level: the logging level to use for this module, e.g., logging.DEBUG or logging.INFO
    :type logging_level: int
    """
    global started
    global logger

    logger.setLevel(logging_level)

    if started is not None:
        logger.info("JVM already running, call jvm.stop() first")
        return

    full_cp = []

    add_lib_dir(root_dir, full_cp)

    # TODO custom WEKA_HOME env var?

    if system_cp:
        logger.debug("Adding system classpath")
        add_system_classpath(full_cp)

    logger.debug("Classpath=" + str(full_cp))

    args = []

    # heapsize
    if max_heap_size is not None:
        logger.debug("MaxHeapSize=%s" % max_heap_size)
        args.append("-Xmx%s" % max_heap_size)
    else:
        logger.debug("MaxHeapSize=default")

    # headless mode
    if headless:
        args.append("-Djava.awt.headless=true")

    jpype.startJVM(*args, classpath=full_cp, convertStrings=convert_strings)
    started = True


def stop():
    """
    Kills the JVM.
    """
    global started
    if started is not None:
        started = None
        jpype.shutdownJVM()
