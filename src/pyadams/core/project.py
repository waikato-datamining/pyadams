import os
import pyadams.core.platform as platform


def project_name() -> str:
    """
    Returns the name of the project.

    :return: the name
    :rtype: str
    """
    return "pyadams"


def project_dir() -> str:
    """
    Returns the director for the pyadams project.

    :return: the directory
    :rtype: str
    """
    if platform.is_linux() or platform.is_mac():
        base_dir = os.path.expanduser("~/.local/share")
    else:
        base_dir = os.path.expanduser("~")

    result = os.path.join(base_dir, project_name())
    return result


def init_project_dir() -> bool:
    """
    Initializes (ie creates) the project directory if necessary.

    :return: True if project is available
    :rtype: bool
    """
    if not os.path.exists(project_dir()):
        os.makedirs(project_dir())
    return os.path.exists(project_dir()) and os.path.isdir(project_dir())
