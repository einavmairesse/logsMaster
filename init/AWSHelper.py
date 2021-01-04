import logging


class AWSHelper:
    @staticmethod
    def install_docker(ssh_client, file_to_log):
        logging.basicConfig(filename=file_to_log)
        logging.info("Starting to install docker")

        apt_update = ssh_client.exec_r
        apt_update_status = apt_update[1].channel.recv_exit_status()

        apt_install = ssh_client.exec_command("sudo apt install containerd -y", get_pty=True)
        apt_install_status = apt_install[1].channel.recv_exit_status()

        install_docker = ssh_client.exec_command("sudo apt-get install docker.io -y", get_pty=True)
        install_docker_status = install_docker.channel.recv_exit_status()

        return install_docker_status

    @staticmethod
    def exec_remote_command(command):
        exec_command = ssh_client.exec_command(command, get_pty=True)
        commands_status = exec_command[1].channel.recv_exit_status()

        return commands_status


