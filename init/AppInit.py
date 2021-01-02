import paramiko


def install_docker(ssh_client):
    print("start installing docker")
    first = ssh_client.exec_command("sudo apt update", get_pty=True)
    apt_update_exit_status = first[1].channel.recv_exit_status()
    second = ssh_client.exec_command("sudo apt install containerd -y", get_pty=True)
    install_containerd_exit_status = second[1].channel.recv_exit_status()
    stdin, stdout, stderr = ssh_client.exec_command("sudo apt-get install docker.io -y", get_pty=True)
    docker_install_exit_status = stdout.channel.recv_exit_status()
    return docker_install_exit_status


def run_app_container(ssh_client):
    stop_running_containers = ssh_client.exec_command("sudo docker stop app", get_pty=True)
    stop_running_containers_status = stop_running_containers[1].channel.recv_exit_status()

    remove_containers = ssh_client.exec_command("sudo docker rm app", get_pty=True)
    remove_containers_status = remove_containers[1].channel.recv_exit_status()

    docker_run_es_container = ssh_client.exec_command(
        "sudo docker run -d -p 5000:5000 --name app logs-master-app", get_pty=True)

    run_es_container_status = docker_run_es_container[1].channel.recv_exit_status()

    for_print = ssh_client.exec_command("sudo docker ps", get_pty=True)
    for_print[1].channel.recv_exit_status()

    print(for_print[1].readlines())
    return run_es_container_status


def build_app_image(ssh_client):
    # cd_logs_master_directory = ssh_client.exec_command("cd /home/ubuntu/logsMaster", get_pty=True)
    # cd_logs_master_directory_status = cd_logs_master_directory[1].channel.recv_exit_status()

    build_app = ssh_client.exec_command("sudo docker build -t logs-master-app /home/ubuntu/logsMaster", get_pty=True)
    build_app_status = build_app[1].channel.recv_exit_status()

    return build_app_status


def clone_app_to_server(ssh_client):
    clone_app = ssh_client.exec_command("git clone https://github.com/einavmairesse/logsMaster", get_pty=True)
    clone_app_status = clone_app[1].channel.recv_exit_status()

    cd_logsmaster = ssh_client.exec_command("cd logsMaster", get_pty=True)
    cd_logsmaster_result = cd_logsmaster[1].channel.recv_exit_status()

    temp_command_checkout = ssh_client.exec_command("git checkout automate-application-deployment", get_pty=True)
    temp_command_checkout_result = temp_command_checkout[1].channel.recv_exit_status()

    return clone_app_status


class AppInit:
    def __init__(self, ip):
        self.ip = ip

    def start_app(self):
        print("starts App")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        privkey = paramiko.RSAKey.from_private_key_file('key')

        ssh.connect(hostname=self.ip, username='ubuntu', pkey=privkey, timeout=20)

        print("connected to App")
        install_docker_result = install_docker(ssh)
        print("docker is installed")
        clone_result = clone_app_to_server(ssh)
        print("project cloned")
        build_app_result = build_app_image(ssh)
        print("image built")
        run_app_container_result = run_app_container(ssh)
        print("container running")
