"""Command module"""
class Command():
    __name__ = "command"

    # Initialisation
    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        # Check params["command"]
        if self.params['command']:
            stdin, stdout, stderr = ssh_client.exec_command(self.params['command'])
            return stdout, stderr.readlines(), stdout.channel.recv_exit_status()