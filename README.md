# App (Broken, needs to be fix)
    docker build -t logs-master-app .
    docker run -d -p 5000:5000 --name app logs-master-app

# Run Elasticsearch instance
    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name es docker.elastic.co/elasticsearch/elasticsearch:6.8.12

# MySQL db
    docker run --name logs-master-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:8.0.21


## How To Run:
1. Run Elasticsearch container

2. Run MySQL Container
    2.1. Connect to MySQL server (with MysqlWorkbench)
        2.1.1. User: root
        2.1.2. Password: password
        2.1.3. Host: 0.0.0.0
        2.1.4. Port: 3306
    2.2. Create a new schema called 'logs-master-db'

3. Go to python console in PyCharm
    3.1. Run `from models import engine, Base`
    3.2. Run `Base.metadata.create_all(engine)`
    3.3. Go to MysqlWorkbench, right click on Tables -> refresh all. See 2 tables created.

4. Run LogsMasterApp.py
    4.1. Make sure everything works by accessing (in browser) http://0.0.0.0:5000/health. You should see the writing "App is running"

## How to call the endpoints:
    # Signup:
        method: post, url: /signup, headers = Content-Type:application/json
        body (example):
            {
                "name": "myUser2111",
                "email": "my2111@email.com",
                "password": "123456"
            }
    # Login:
        method: post, url: /login, headers = Content-Type:application/json
        body:
            {
                "email": "my2111@email.com",
                "password": "123456"
            }
<!--     # Send Logs: -->
        method: post, url: /send_logs, headers = Content-Type:application/json
        body:
        {
            "token": "{token-received-from-login}",
            "logs": [
                {
                    "key1": "value1",
                    "timestamp1": "timestamp1_value"
                },
                {
                    "key2": "value2",
                    "timestamp2": "timestamp2_value"
                }
            ]
        }

    # Search Logs:
        method: post, url: /send_logs, headers = Content-Type:application/json
        {
            "token": "{token-received-from-login}",
            "query": {"match_all": {}}
        }