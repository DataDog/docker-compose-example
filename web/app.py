from flask import Flask
from redis import Redis
import os

# Add and initialize Datadog monitoring.
from datadog import initialize, statsd
initialize(statsd_host=os.environ.get('DATADOG_HOST'))


app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    # Increment the Datadog counter.
    statsd.increment('docker_compose_example.page.views')

    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
