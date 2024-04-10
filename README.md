# 📊🏠🔌☀ HomeAssistant Huawei SUN2000 Exporter

[Prometheus][1] exporter providing metrics from a HomeAssistant instance about a
Huawei SUN2000 inverter.

## Why?

- HomeAssistant's Prometheus integration is currently broken (see [issue #80656][2]
  and [issue #104803][3] for example).
- The SUN2000's TCP modbus interface can always just talk to *one* single client
  at a time, therefore using a direct modbus connection to the inverter would
  interfere with HomeAssistant's data scraping.
- HomeAssistant provides stats through its built-in API anyway, so let's use them.

Until there is a better solution, this workaround does the job.

## ⚙🔧 How? ⚙🔧

Example installation on Debian / Ubuntu:

```bash
### all commands run as "root" or using "sudo" ###

# required for creating Python virtualenvs:
apt update
apt install -y python3-venv

# create a virtualenv in /opt:
python3 -m venv /opt/prometheus-hass-sun2k

# update 'pip' and install the 'prometheus-hass-sun2k' package:
/opt/prometheus-hass-sun2k/bin/pip install --upgrade pip
/opt/prometheus-hass-sun2k/bin/pip install prometheus-hass-sun2k
```

## 🏃 Running in foreground mode 🏃

Create a configuration file by copying the [config-example.yaml][4] file to e.g.
`config.yaml` and adjust the settings there. Then run the exporter (from within
the activated venv or using the full path) like this:

```bash
prometheus-hass-sun2k -vvv --config config.yaml
```

The exporter running in foreground can be terminated as usual via `Ctrl+C`.

## 👟 Running as a service 👟

```bash
# create a system user for running the service:
adduser --system --group has2k-exporter

# install, register and adjust the systemd unit file:
cp -v /opt/prometheus-hass-sun2k/lib/python*/site-packages/resources/systemd/prometheus-hass-sun2k.service  /etc/systemd/system/
systemctl daemon-reload
systemctl edit prometheus-hass-sun2k.service
```

The last command will open an editor with the override configuration of the
service's unit file. Check the values from the provided example script (e.g.
paths) and adjust as necessary.

Finally enable the service and start it right away. The second line will show
the log messages on the console until `Ctrl+C` is pressed. This way you should
be able to tell if the service has started up properly and is providing metrics
on the configured port:

```bash
systemctl enable --now prometheus-hass-sun2k.service
journalctl --follow --unit prometheus-hass-sun2k
```

[1]: https://prometheus.io/
[2]: https://github.com/home-assistant/core/issues/80656
[3]: https://github.com/home-assistant/core/issues/104803
[4]: resources/config-example.yaml
