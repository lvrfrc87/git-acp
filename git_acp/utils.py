import os
import sys
import stat
import shutil
import tempfile
import subprocess

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


def write_ssh_wrapper():
    tmpdir = tempfile.TemporaryDirectory()
    try:
        if os.access(tmpdir.name, os.W_OK | os.R_OK | os.X_OK):
            fd, wrapper_path = tempfile.mkstemp(prefix=tmpdir.name + "/")
        else:
            raise OSError
    except (IOError, OSError):
        fd, wrapper_path = tempfile.mkstemp()

    fh = os.fdopen(fd, "w+b")
    template = """
    #!/bin/sh
    if [ -z "$GIT_SSH_OPTS" ]; then
        BASEOPTS=""
    else
        BASEOPTS=$GIT_SSH_OPTS
    fi

    # Let ssh fail rather than prompt
    BASEOPTS="$BASEOPTS -o BatchMode=yes"

    if [ -z "$GIT_KEY" ]; then
        ssh $BASEOPTS "$@"
    else
        ssh -i "$GIT_KEY" -o IdentitiesOnly=yes $BASEOPTS "$@"
    fi
    """.encode(
        "UTF-8"
    )
    fh.write(template)
    fh.close()
    st = os.stat(wrapper_path)
    os.chmod(wrapper_path, st.st_mode | stat.S_IEXEC)
    return wrapper_path, tmpdir


def set_git_ssh(ssh_wrapper, key_file, ssh_opts):
    if os.environ.get("GIT_SSH"):
        del os.environ["GIT_SSH"]
    os.environ["GIT_SSH"] = ssh_wrapper

    if os.environ.get("GIT_KEY"):
        del os.environ["GIT_KEY"]

    if key_file:
        os.environ["GIT_KEY"] = key_file

    if os.environ.get("GIT_SSH_OPTS"):
        del os.environ["GIT_SSH_OPTS"]

    if ssh_opts:
        os.environ["GIT_SSH_OPTS"] = ssh_opts

def run_command(command, cwd):
    pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = pipes.communicate()
    rc = pipes.returncode
    return rc, stdout, stderr