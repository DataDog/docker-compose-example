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
version: "2"
services:
  web:
    build: web
    command: python app.py
    ports:
     - "5000:5000"
    volumes:
     - ./web:/code # modified here to take into account the new app path
    links:
     - redis
    environment:
     - DATADOG_HOST=datadog # used by the web app to initialize the Datadog library
  redis:
    image: redis
  # agent section
  datadog:
    build: datadog
    links:
     - redis # ensures that redis is a host that the container can find
     - web # ensures that the web app can send metrics
    environment:
     - API_KEY=__your_datadog_api_key_here__
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /proc/:/host/proc/:ro
     - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
```

# Configuring the Agent

Because the Agent needs to monitor redis it needs:

1. the proper `redisdb.yaml` in the container's `/etc/dd-agent/conf.d`
1. to find the redis node.

The Agent's `Dockerfile` takes care of #1.

```
FROM datadog/docker-dd-agent
ADD conf.d/redisdb.yaml /etc/dd-agent/conf.d/redisdb.yaml
```

And the Compose yaml files creates the link to redis with:

```yaml
  links:
    - redis
```

# All in one

How to test this?

1. [Install Docker Compose](https://docs.docker.com/compose/install/)
1. Clone this repository
1. Update your `API_KEY` in `docker-compose.yml`
1. Run all containers with `docker-compose up`
1. Verify in Datadog that your container picks up the docker and redis metrics
