"""Sysctl module"""

class Sysctl:
    __name__ = "sysctl"

    # Initialization
    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        # Initialisation value
        attribute: str = self.params['attribute']
        value: any = self.params['value']
        permanent: bool = self.params['permanent']

        # Check permenent
        if permanent:
            response = f' sudo bash -c \'echo "{attribute} = {value}" >> /etc/sysctl.conf && sudo sysctl -p ' \
                       f'/etc/sysctl.conf\' '
        else:
            response = f'sudo sysctl -w {attribute}={value}'

        stdin, stdout, stderr = ssh_client.exec_command(response)

        return stdout, stderr.readlines(), stdout.channel.recv_exit_status()