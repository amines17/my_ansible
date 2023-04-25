"""Template module"""
from jinja2 import Template


class Templates:
    __name__ = "template"

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        # Initialisation value
        src = self.params['src']
        dest = self.params['dest']
        vars = self.params.get("vars", None)

        # Open file
        with open(src, 'r') as file:
            file_ = Template(file.read())

        # Reading file
        render = file_.render(vars)
        # Send file to VM
        stdin, stdout, stderr = ssh_client.exec_command(
            f'sudo mkdir -p {dest}; sudo bash -c \'echo "{render}" > {dest}\''
        )

        return stdout, stderr.readlines(), stdout.channel.recv_exit_status()
