"""Apt module"""
from paramiko.client import SSHClient


class Apt:
    __name__ = "apt"

    def __init__(self, params: dict):
        self.params = params
    # Function process module apt
    def process(self: dict, ssh_client: SSHClient):
        apt_ = self.params['name']
        # Check state
        if self.params['state'] == 'present':
            # Execute command
            stdin, stdout, stderr = ssh_client.exec_command(f'sudo apt install --yes {apt_}')

        if self.params['state'] == 'absent':
            stdin, stdout, stderr = ssh_client.exec_command(f'sudo apt remove --yes {apt_}')
        # Return stdout, stderr
        return stdout, stderr.readlines(), stdout.channel.recv_exit_status()
