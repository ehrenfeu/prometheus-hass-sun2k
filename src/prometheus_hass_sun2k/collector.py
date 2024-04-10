"""Metrics collection classes."""

import json

from loguru import logger as log
from requests import get


def map_unit(unit):
    if unit == "%":
        return "ratio"
    if unit == "°C":
        return "celsius"
    if unit == "V":
        return "volts"
    if unit == "A":
        return "amperes"
    if unit == "W":
        return "watts"
    if unit == "Hz":
        return "hertz"

    return unit


def fetch_entity_state(name, config):
    url = f"{config.homeassistant.api_url}/states/{config.entity_pfx}_{name}"
    headers = {
        "Authorization": f"Bearer {config.homeassistant.token}",
        "content-type": "application/json",
    }
    log.trace(f"Requesting [{url}]...")
    response = get(url, headers=headers, timeout=10)
    state = json.loads(response.text)
    return state


def new_metric(state, metric_type, config):
    cut = len(config.entity_pfx) + 1
    name = state["entity_id"][cut:]
    attributes = state["attributes"]
    try:
        unit = map_unit(attributes["unit_of_measurement"])
    except KeyError:
        unit = ""
    docs = attributes["friendly_name"]
    prefix = config.metric_pfx
    return metric_type(name=f"{prefix}_{name}", documentation=docs, unit=unit)
