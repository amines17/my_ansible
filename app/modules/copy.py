"""Copy module"""
import os


class Copy:
    __name__ = 'copy'

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        # Initialisation value
        src = self.params['src']
        dest = self.params['dest']
        backup = self.params.get('backup', False)
        error = ""
        res = 0

        # Check backup exist => copie file with "_backup" in VM
        if backup:
            ssh_client.exec_command(f'sudo cp -r {dest} {dest}_backup')

        # Check file / directory
        is_dir = os.path.isdir(src)

        # Create file in VM
        ssh_client.exec_command(f'sudo mkdir -p {dest} && sudo chmod 777 {dest}')

        # Write files
        sftp = ssh_client.open_sftp()

        # Import files (src) and send to dest (VM)
        if is_dir:
            for filename in os.listdir(src):
                try:
                    # téléchargement fichier dans la VM
                    sftp.put(f'{src}/{filename}', f'{dest}/{filename}')
                except IOError as e:
                    error = e
                    res = 1
        else:
            try:
                sftp.put(src, dest)
            except IOError as e:
                error = e
                res = 1

        sftp.close()

        return None, error, res
