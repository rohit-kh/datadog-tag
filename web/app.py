from flask import Flask
from redis import Redis
from ddtrace import tracer
import os

# Add and initialize Datadog monitoring.
from datadog import initialize, statsd
initialize(statsd_host=os.environ.get('DATADOG_HOST'))

tracer.configure(
    hostname=os.environ.get('DATADOG_HOST'),
    port="8126",
)

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    # Increment the Datadog counter.
    statsd.increment('docker_compose_example.page.views')

    current_span = tracer.current_span()
    if current_span:
        current_span.set_tag('customer', 'customer-name')

    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
