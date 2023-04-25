"""Main file"""
import logging

import click as click
import yaml
from paramiko.client import SSHClient

from modules.apt import Apt
from modules.command import Command
from modules.copy import Copy
from modules.service import Service
from modules.sysctl import Sysctl
from modules.template import Templates
from ssh.ssh_authentication import Ssh

# Initialisation logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - root - %(levelname)s - %(message)s',
)

# Function which return a right module
def call_module(name: str, params):
    if name == "copy":
        return Copy(params)
    elif name == "apt":
        return Apt(params)
    elif name == "template":
        return Templates(params)
    elif name == "sysctl":
        return Sysctl(params)
    elif name == "service":
        return Service(params)
    elif name == "command":
        return Command(params)

# Function to execute commands to Host
def run_remote_cmd(command: str, ssh_client: SSHClient, config: dict):
    module = call_module(command, config)

    return module.process(ssh_client)

# Function call task execute task for each module
# Return total hosts, ok, ko
def call_task(file: str, ssh_client: SSHClient):
    # INitialisation value
    count = 0
    ok = 0
    ko = 0
    # get host address
    hostname, _ = ssh_client.get_transport().getpeername()

    # For each module and params, execute command
    for item in file:
        module = item['module']
        params = item['params']

        count += 1

        logging.info(f'[{count}] hosts={hostname} op={module} params={params}')

        stdout, stderr, res = run_remote_cmd(module, ssh_client, params)

        # Check success, fail and error
        if res == 0:
            logging.info(f'{hostname} op={module} status=OK')
            ok += 1
        else:
            error = ''.join(stderr)
            logging.info(f'{hostname} op={module} status=KO')
            logging.info(f'Error: {error}')
            ko += 1

    return {
        "host": hostname,
        "ok": ok,
        "ko": ko
    }

@click.command()
@click.option('-f', help='List of todo')  # to do test_yaml
@click.option('-i', help='List of hosts')  # inventory test_config
# Main function
def main(f, i):
    file = f
    arg = i

    # Open file .yaml
    with open(file) as files:
        file = yaml.load(files, Loader=yaml.FullLoader)

    with open(arg) as args:
        arg = yaml.load(args, Loader=yaml.FullLoader)

    # Connexion hosts
    connect_host = Ssh.connect(arg['hosts'])
    hosts = ""

    # Loop to retrieve total tasks and hosts
    for item in arg['hosts']:
        for key, value in item.items():
            hosts += value['address'] + ' '

    logging.info(f'processing {len(file)} tasks on hosts: {hosts}')

    res = []
    # Loop to execute for each host all tasks
    for host in connect_host:
        response = call_task(file, host)
        res.append(response)
        host.close()
    logging.info(f'done processing tasks for hosts: {hosts}')

    # Loop for logging info
    for item in res:
        logging.info(f'host={item["host"]} ok={item["ok"]} ko={item["ko"]}')


if __name__ == '__main__':
    main()
