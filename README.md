# Prometheus exporter for HomeAssistant data on SUN2000 inverters

## Why?

- HomeAssistant's Prometheus integration is currently broken.
- The SUN2000's TCP modbus interface can always just talk to a single client
  at a time, therefore using a direct modbus connection to the inverter would
  interfere with HA's data scraping.
- HA provides stats through its built-in API anyway.

Until there is a better solution, this workaround does the job.

## How?

! FIXME !

1. pip install
1. create config
1. create system user
1. install systemd unit file
