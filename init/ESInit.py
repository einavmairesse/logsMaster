import docker
client = docker.from_env()

client.containers.run("docker.elastic.co/elasticsearch/elasticsearch:6.8.12", None,
                      ports={'9200/tcp': 9200, '9300/tcp': 9300}, name="es",
                      environment=['ES_JAVA_OPTS="-Xms100m -Xmx100m"', 'discovery.type=single-node'])