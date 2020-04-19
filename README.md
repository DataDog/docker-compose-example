# Using Docker Compose with Datadog

Datadog offers native Docker container monitoring, either by running the Agent
on the host or running in a sidecar container. Which is the best way to run it?
It ultimately depends on the tooling you have in place to manage the Agent's
configuration. If you want to go Docker all the way, you can run the Agent as
a sidecar and control its configuration with custom `Dockerfiles`.

Let's see what it looks like.

# Starting off from the Compose example

To build a meaningful setup, we start from the [example](https://docs.docker.com/compose/#overview)
that Docker put together to illustrate Compose. A simple python web application that
connects to Redis to store the number of hits.

Here is the `docker-compose.yml` that powers the whole setup.

```yaml
version: "3"
services:
  web:
    build: web
    command: python app.py
    ports:
     - "5000:5000"
    volumes:
     - ./web:/code # modified here to take into account the new app path
    environment:
     - DATADOG_HOST=datadog # used by the web app to initialize the Datadog library
  redis:
    image: redis
    ports:
     - "6379:6379"
  # agent section
  datadog:
    build: datadog
    environment:
     - DD_API_KEY=__your_datadog_api_key_here__
     - DD_DOGTAND_NON_LOCAL_TRAFFIC=true
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /proc/:/host/proc/:ro
     - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
    ports:
     - "8125:8125/udp"
```

# Configuring the Agent

Because the Agent needs to monitor redis it needs:

1. the proper `redisdb.yaml` in the container's `/etc/datadog-agent/conf.d`
1. to find the redis node.

The Agent's `Dockerfile` takes care of #1.

```
FROM datadog/agent:latest
ADD conf.d/redisdb.yaml /etc/datadog-agent/conf.d/redisdb.yaml
```

And the Compose yaml files opens the port on the host for other containers to connect to:

```yaml
  ports:
   - "8125:8125/udp"
```

# All in one

How to test this?

1. [Install Docker Compose](https://docs.docker.com/compose/install/)
1. Clone this repository
1. Update your `DD_API_KEY` in `docker-compose.yml`
1. Run all containers with `docker-compose up`
1. Verify in Datadog that your container picks up the docker and redis metrics
