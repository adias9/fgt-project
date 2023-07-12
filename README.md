## Flask sample application

### Python/Flask with PostgreSQL database

Project structure:
```
.
├── compose.yaml
└── flask
    ├── Dockerfile
    ├── requirements.txt
    └── server.py

```

[_compose.yaml_](compose.yaml)
```
services:
  flask_app:
    build: .
    ...
  flask_db:
    image: postgres:12
    ...
```
The compose file defines an application with two services `backend` and `db`.
When deploying the application, docker compose maps port 4000 of the proxy service container to port 4000 of the host as specified in the file.
Make sure port 4000 on the host is not already being in use.

## Deploy with docker compose

```
$ docker compose up -d
Building 1.0s (11/11) FINISHED
...
...
WARNING: Image for service proxy was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
 ✔ Network fgt-project_default  Created
 ✔ Container flask_db           Started
 ✔ Container flask_app          Started
```

## Expected result

Listing containers should show three containers running and the port mapping as below:
```
$ docker compose ps
NAME                IMAGE                                  COMMAND                  SERVICE             CREATED             STATUS              PORTS
flask_app           andreasmodsquad/flask_live_app:1.0.0   "flask run --host=0.…"   flask_app           3 minutes ago       Up 3 minutes        0.0.0.0:4000->4000/tcp
flask_db            postgres:12                            "docker-entrypoint.s…"   flask_db            3 minutes ago       Up 3 minutes        0.0.0.0:5432->5432/tcp
```

After the application starts, navigate to `http://localhost:4000` in your web browser or run:
```
$ curl localhost:4000
{ "message": "hello world" }
```

Stop and remove the containers
```
$ docker compose down
```

