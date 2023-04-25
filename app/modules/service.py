"""Service module"""

class Service:
    __name__ = "service"

    # Initialisation
    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        # Initialisation value
        service_ = self.params['name']
        state = {
            'started': 'start',
            'restarted': 'restart',
            'stopped': 'stop',
            'enabled': 'enable',
            'disabled': 'disable'
        }
        # Writing in terminal
        stdin, stdout, stderr = ssh_client.exec_command(f'sudo service {service_} {state}')

        #stdout response du terminal, stderr renvoie les erreur
        # Channel.recv => tout programme envoie un code de sortie la valeur de la sortie du programme 0
        return stdout, stderr.readlines(), stdout.channel.recv_exit_status()

