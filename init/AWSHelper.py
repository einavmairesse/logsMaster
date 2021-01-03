class AWSHelper:
    @staticmethod
    def install_docker(ssh_client):
        print("start installing docker")
        first = ssh_client.exec_command("sudo apt update", get_pty=True)
        apt_update_exit_status = first[1].channel.recv_exit_status()
        second = ssh_client.exec_command("sudo apt install containerd -y", get_pty=True)
        install_containerd_exit_status = second[1].channel.recv_exit_status()
        stdin, stdout, stderr = ssh_client.exec_command("sudo apt-get install docker.io -y", get_pty=True)
        docker_install_exit_status = stdout.channel.recv_exit_status()
        return docker_install_exit_status


