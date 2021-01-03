import paramiko

from init.AWSHelper import AWSHelper


class ESInit:
    def __init__(self, ip):
        self.ip = ip

    def start_es(self):
        print("starts es")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        privkey = paramiko.RSAKey.from_private_key_file('key')

        ssh.connect(hostname=self.ip, username='ubuntu', pkey=privkey, timeout=20)

        print("connected to db")
        install_docker_result = AWSHelper.install_docker(ssh)
        print("docker is installed")
        run_es_container_result = self.run_es_container(ssh)
        print("container running")

    def run_es_container(self, ssh_client):
        stop_running_containers = ssh_client.exec_command("sudo docker stop $(sudo docker ps -a)", get_pty=True)
        stop_running_containers_ststus = stop_running_containers[1].channel.recv_exit_status()

        remove_containers = ssh_client.exec_command("sudo docker rm $(sudo docker ps -a)", get_pty=True)
        remove_containers_status = remove_containers[1].channel.recv_exit_status()

        docker_run_es_container = ssh_client.exec_command(
            "sudo docker run -p 9200:9200 -p 9300:9300 -e ES_JAVA_OPTS=\"-Xms100m -Xmx100m\""
            " -e \"discovery.type=single-node\" "
            "--name es docker.elastic.co/elasticsearch/elasticsearch:6.8.12 &",
            get_pty=True)

        run_es_container_status = docker_run_es_container[1].channel.recv_exit_status()

        for_print = ssh_client.exec_command("sudo docker ps", get_pty=True)
        for_print[1].channel.recv_exit_status()

        print(for_print[1].readlines())
        return run_es_container_status


