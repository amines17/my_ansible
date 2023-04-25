import logging

import paramiko
from paramiko.client import SSHClient


class Ssh:
    def connect(file: str):
        hosts = []
        for item in file:
            for key, value in item.items():
                hostname = value.get('address')
                port = value.get('port', None)
                username = value.get('username', key)
                password = value.get('password', None)
                key_filename = value.get('key_filename', None)

                client = SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=hostname, port=port, username=username, password=password,
                               key_filename=key_filename)
                hosts.append(client)
        return hosts
