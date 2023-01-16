import sys

class ModuleFailure:
    def __init__(self, rc, command, output, error):
        """
        Failing message function for rc codes != 0.
        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
            * rc:
                type: int()
                descrition: rc code returned by shell command.
            * command:
                type: list()
                descrition: list of string that compose the shell command.
            * output:
                type: str()
                descrition: stdout returned by the shell.
            * error:
                type: str()
                descrition: stderreturned by the shell.
        return: None
        """
        print({"rc": rc, "command":command, "output":output, "error": error})
        sys.exit(1)

class FailingMessage(ModuleFailure):
    """Module failure related errors."""
