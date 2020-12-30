import docker

import paramiko as paramiko


def wait_exec_command(stdout):
    stdout_lines = None
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            stdout_lines = stdout.readlines()

    return stdout_lines


def apt_update(ssh_client):
    stdin, stdout, stderr = ssh_client.exec_command("sudo apt update", get_pty=True)
    return stdin, stdout, stderr


def pip3_install(ssh_client):
    first = ssh_client.exec_command("sudo apt -f install", get_pty=True)
    apt_exit_status = first[1].recv_exit_status()
    second = ssh_client.exec_command("sudo apt update && sudo apt dist-upgrade -y", get_pty=True)
    apt_update_exit_status = second[1].recv_exit_status()
    stdin, stdout, stderr = ssh_client.exec_command("sudo apt install python3-pip -y", get_pty=True)
    docker_exit_status = stdout.recv_exit_status()

    return stdin, stdout, stderr


def install_docker(ssh_client):
    print("start installing docker")
    first = ssh_client.exec_command("sudo apt update", get_pty=True)
    apt_update_exit_status = first[1].channel.recv_exit_status()
    second = ssh_client.exec_command("sudo apt install containerd -y", get_pty=True)
    install_containerd_exit_status = second[1].channel.recv_exit_status()
    stdin, stdout, stderr = ssh_client.exec_command("sudo apt-get install docker.io -y", get_pty=True)
    docker_install_exit_status = stdout.channel.recv_exit_status()
    return wait_exec_command(stdout)


def run_sql_container(ssh_client):
    first = ssh_client.exec_command("sudo docker run --name logs-master-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password"
                                    " -d mysql:8.0.21", get_pty=True)
    apt_update_exit_status = first[1].channel.recv_exit_status()
    return apt_update_exit_status


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
        # pip3_install_result = pip3_install(ssh)
        # print("pip3 is installed")
        install_docker_result = install_docker(ssh)
        print("docker is installed")
        run_sql_container_result = run_sql_container(ssh)
        print("container running")


    def _install_docker_py(self):
       print("install docker- demo")

    def _run_mysql_container(self):
        client = docker.from_env()
        client.containers.run("mysql:8.0.21", None, ports={'3306/tcp': 3306}, name="logs-master-db",
                              environment=["MYSQL_ROOT_PASSWORD=password"])

