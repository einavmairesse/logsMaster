import docker
import subprocess as sp


class DBInit:
    def __init__(self, ip):
        self.ip = ip

    def start_db(self):
        self._install_docker_py()

    def _install_docker_py(self):
       print("install docker- demo")

    def _run_mysql_container(self):
        client = docker.from_env()
        client.containers.run("mysql:8.0.21", None, ports={'3306/tcp': 3306}, name="logs-master-db",
                              environment=["MYSQL_ROOT_PASSWORD=password"])

