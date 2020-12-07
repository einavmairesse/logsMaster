import docker
client = docker.from_env()

client.images.build(path="../")
client.api.create_container("logs-master-app", ports={5000: 5000})
