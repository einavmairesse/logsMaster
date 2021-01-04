import logging

import paramiko as paramiko

from init.AWSHelper import AWSHelper
import logging

file_name = "MsqlInit.log"
logging.basicConfig(filename=file_name, level=logging.INFO)


class DBInit:
    def __init__(self, ip):
        self.ip = ip

    def start_db(self):
        logging.info("Starting to initialize server")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        privkey = paramiko.RSAKey.from_private_key_file('key')

        try:
            ssh.connect(hostname=self.ip, username='ubuntu', pkey=privkey, timeout=20)
        except TimeoutError as e:
            logging.error("An error occur while trying to connect to Mysql instances: %s", e)
            exit(-1)

        logging.info("Connected to Mysql instance")

        install_docker_result = AWSHelper.install_docker(ssh, file_name)
        run_sql_container_result = self.run_sql_container(ssh)

    def run_sql_container(self, ssh_client):
        first = ssh_client.exec_command(
            "sudo docker run --name logs-master-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password"
            " -d mysql:8.0.21", get_pty=True)
        apt_update_exit_status = first[1].channel.recv_exit_status()
        return apt_update_exit_status


