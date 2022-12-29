import sys
import shutil


def get_bin_path(executable):
    """
    Find system executable in PATH. Raises ValueError if executable is not found.
    """
    exec = shutil.which(executable)
    if not exec:
        raise ValueError(
            f"Failed to find required executable {executable} in $PATH: {sys.path}"
        )
    return exec
