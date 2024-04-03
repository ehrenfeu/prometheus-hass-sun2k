# Prometheus exporter for HomeAssistant data on SUN2000 inverters

## Why?

- HomeAssistant's Prometheus integration is currently broken.
- The SUN2000's TCP modbus interface can always just talk to a single client
  at a time, therefore using this would interfere with HA's data scraping.
- HA provides stats through it's built-in API.

Until there is a better solution, this workaround does the job.

## How?

1. Clone this repo.
1. Update `settings.py`.
1. Create an API token in your HA instance.
1. Place the token in the `cred.py` file:

```Python
# cred.py
API_URL = "https://my-homeassistant.local:8124/api"
TOKEN = "PutYourPreviouslyCreatedTokenHere"
```

Then create a `venv`, install the requirements and run the collector:

```bash
python3 -m venv venv
venv/bin/pip install --upgrade pip requests prometheus-client
venv/bin/python collector_hass_api.py
```

