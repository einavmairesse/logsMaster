import docker
client = docker.from_env()

client.images.build(path="../")
client.containers.run("logs-master-app", None, ports={'5000/tcp': 5000}, name="app")
