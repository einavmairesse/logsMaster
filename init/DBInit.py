import docker
client = docker.from_env()

client.containers.run("mysql:8.0.21", None, ports={'3306/tcp': 3306}, name="logs-master-db",
                      environment=["MYSQL_ROOT_PASSWORD=password"])
