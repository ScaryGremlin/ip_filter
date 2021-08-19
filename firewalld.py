from paramiko import SSHClient, AutoAddPolicy

import creds


def add_firewalld_rule():

    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(creds.SSH_HOST, creds.SSH_PORT)
        ssh_client.exec_command("")
