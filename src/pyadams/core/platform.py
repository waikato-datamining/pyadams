import sys


def is_linux() -> bool:
    """
    Returns whether this is a Linux machine.

    :return: True if Linux
    :rtype: bool
    """
    return sys.platform == "linux"


def is_windows() -> bool:
    """
    Returns whether this is a Windows machine.

    :return: True if Windows
    :rtype: bool
    """
    return sys.platform == "win32"


def is_mac() -> bool:
    """
    Returns whether this is a Mac machine.

    :return: True if Mac
    :rtype: bool
    """
    return sys.platform == "darwin"
