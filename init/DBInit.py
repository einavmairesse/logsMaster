import docker

import paramiko as paramiko

from init.AWSHelper import AWSHelper


class DBInit:
    def __init__(self, ip):
        self.ip = ip

    def start_db(self):
        print("starts db")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        privkey = paramiko.RSAKey.from_private_key_file('key')

        ssh.connect(hostname=self.ip, username='ubuntu', pkey=privkey, timeout=20)

        print("connected to db")
        install_docker_result = AWSHelper.install_docker(ssh)
        print("docker is installed")
        run_sql_container_result = self.run_sql_container(ssh)
        print("container running")

    def run_sql_container(self, ssh_client):
        first = ssh_client.exec_command(
            "sudo docker run --name logs-master-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password"
            " -d mysql:8.0.21", get_pty=True)
        apt_update_exit_status = first[1].channel.recv_exit_status()
        return apt_update_exit_status


