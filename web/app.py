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


@app.route('/supply_branding')
def supply_branding():
    current_span = tracer.current_span()
    if current_span:
        current_span.set_tag('product', 'supply_branding')
    redis.incr('supply.branding.view')
    return 'Hello World! I have been seen %s times.' % redis.get('supply.branding.view')



@app.route('/supply_storefront')
def supply_storefront():
    current_span = tracer.current_span()
    if current_span:
        current_span.set_tag('product', 'supply_storefront')
    redis.incr('supply.storefront.view')
    return 'Hello World! I have been seen %s times.' % redis.get('supply.storefront.view')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
