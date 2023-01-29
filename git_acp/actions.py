from utils import get_bin_path, write_ssh_wrapper, set_git_ssh, run_command
from messages import failing_message
import json

class Git:
    def __init__(self, **kwargs):

        self.url = kwargs["url"]
        self.path = kwargs.get("path", ".")
        self.git_path = kwargs.get("executable", get_bin_path("git"))
        self.add_file = kwargs.get("add", ".")
        self.comment = kwargs.get("comment")
        self.mode = kwargs.get("mode", "https")
        self.branch = kwargs.get("branch", "main")
        self.remote = kwargs.get("remote", "origin")
        self.push_option = kwargs.get("push_option")
        self.user = kwargs.get("user")
        self.token = kwargs.get("token")
        ssh_params = kwargs.get("ssh_params")

        if ssh_params:
            self.ssh_key_file = (
                ssh_params["key_file"] if "key_file" in ssh_params else None
            )
            self.ssh_opts = ssh_params["ssh_opts"] if "ssh_opts" in ssh_params else None
            self.ssh_accept_hostkey = (
                ssh_params["accept_hostkey"]
                if "accept_hostkey" in ssh_params
                else False
            )
            if self.ssh_accept_hostkey:
                if self.ssh_opts is not None:
                    if "-o StrictHostKeyChecking=no" not in self.ssh_opts:
                        self.ssh_opts += " -o StrictHostKeyChecking=no"
                else:
                    self.ssh_opts = "-o StrictHostKeyChecking=no"

            self.ssh_wrapper, self.tmpdir = write_ssh_wrapper()
            set_git_ssh(self.ssh_wrapper, self.ssh_key_file, self.ssh_opts)
            self.tmpdir.cleanup()

    

    def add(self):
        """
        Run git add and stage changed files.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.

        return: null
        """

        command = [self.git_path, "add", "--"]
        command.append(self.add_file)
        rc, output, error = run_command(command, cwd=self.path)
        if rc == 0:
            return
        raise Exception(json.dumps(failing_message(rc, command, output, error), indent=4))

    def status(self):
        """
        Run git status and check if repo has changes.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * data:
                type: set()
                description: list of files changed in repo.
        """
        data = set()
        command = [self.git_path, "status", "--porcelain"]

        rc, output, error = run_command(command, cwd=self.path)

        if rc == 0:
            for line in output.split("\n"):
                file_name = line.split(" ")[-1].strip()
                if file_name:
                    data.add(file_name)
            return data

        else:
            raise Exception(json.dumps(failing_message(rc, command, output, error), indent=4))

    def commit(self):
        """
        Run git commit and commit files in repo.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * result:
                type: dict()
                desription: returned output from git commit command and changed status
        """
        result = dict()
        command = [self.git_path, "commit", "-m", self.comment]

        rc, output, error = run_command(command, cwd=self.path)

        if rc == 0:
            if output:
                result.update({"git_commit": output, "changed": True})
                return result
        else:
            raise Exception(json.dumps(failing_message(rc, command, output, error), indent=4))

    def push(self):
        """
        Set URL and remote if required. Push changes to remote repo.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * result:
                type: dict()
                desription: returned output from git push command and updated changed status.
        """

        def set_url():
            """
            Set URL and remote if required.

            args:
                * module:
                    type: dict()
                    descrition: Ansible basic module utilities and module arguments.
            return: null
            """
            command = [self.git_path, "remote", "get-url", "--all", self.remote]

            rc, output, _error = run_command(command, cwd=self.path)

            if rc == 128:
                if self.mode == "https":
                    if self.url.startswith("https://"):
                        command = [
                            self.git_path,
                            "remote",
                            "add",
                            self.remote,
                            f"https://{self.user}:{self.token}@{self.utl[:8]}",
                        ]
                    else:
                        raise Exception("HTTPS mode selected but not HTTPS URL provided")
                else:
                    command = [self.git_path, "remote", "add", self.remote, self.url]

                rc, output, error = run_command(command, cwd=self.path)

                if rc == 0:
                    return

            elif rc == 0 and output != self.url:
                command = ["git", "remote", "remove", self.remote]
                rc, output, error = run_command(command, cwd=self.path)
                if rc == 0:
                    if self.mode == "https":
                        if self.url.startswith("https://"):
                            command = [
                                self.git_path,
                                "remote",
                                "add",
                                self.remote,
                                f"https://{self.user}:{self.token}@{self.url[8:]}",
                            ]
                        else:
                            self.module.fail_json(
                                msg="HTTPS mode selected but no HTTPs URL provided"
                            )
                    else:
                        command = [self.git_path, "remote", "add", self.remote, self.url]

                    rc, output, error = self.module.run_command(command, cwd=self.path)
                    if rc == 0:
                        return
                    raise Exception(json.dumps(failing_message(rc, command, output, error), indent=4))
                else:
                    raise Exception(json.dumps(failing_message(rc, command, output, error), indent=4))

            elif rc == 0:
                return

        def push_cmd():
            """
            Set URL and remote if required. Push changes to remote repo.

            args:
                * path:
                    type: path
                    descrition: git repo local path.
                * cmd_push:
                    type: list()
                    descrition: list of commands to perform git push operation.
            return:
                * result:
                    type: dict()
                    desription: returned output from git push command and updated changed status.
            """
            result = dict()

            rc, output, error = self.module.run_command(command, cwd=self.path)

            if rc == 0:
                result.update({"git_push": str(error) + str(output), "changed": True})
                return result
            else:
                FailingMessage(self.module, rc, command, output, error)

        command = [self.git_path, "push", self.remote, self.branch]

        if self.push_option:
            command.insert(3, f"--push-option={self.push_option}")

        set_url()

        return push_cmd()
