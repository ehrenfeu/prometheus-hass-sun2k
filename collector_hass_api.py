import json
from time import sleep

from requests import get
from prometheus_client import start_http_server, Info, Gauge, Counter

from settings import (
    SCRAPE_INTERVAL,
    METRIC_PFX,
    ENTITY_PFX,
    PORT,
    ADDR,
    TOKEN,
    API_URL,
    HEADERS,
    GAUGE_NAMES,
    COUNTER_NAMES,
)

def prepare_export():
    start_http_server(port=PORT, addr=ADDR)
    info = Info(
        name=f"{METRIC_PFX}_collector",
        documentation="SUN2000 inverter series metrics collector (via HomeAssistant)",
    )


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


def fetch_entity_state(name):
    url = f"{API_URL}/states/{ENTITY_PFX}_{name}"
    # print(f"Requesting [{url}]...")
    response = get(url, headers=HEADERS)
    state = json.loads(response.text)
    return state


def new_metric(state, metric_type):
    cut = len(ENTITY_PFX) + 1
    name = state["entity_id"][cut:]
    attributes = state["attributes"]
    try:
        unit = map_unit(attributes["unit_of_measurement"])
    except KeyError:
        unit = ""
    docs = attributes["friendly_name"]
    return metric_type(name=f"{METRIC_PFX}_{name}", documentation=docs, unit=unit)


def run_loop():
    counters = {}
    gauges = {}

    while True:
        print("Updating metrics...")

        print("Processing counters...")
        for name in COUNTER_NAMES:
            state = fetch_entity_state(name)
            if name not in counters:
                counters[name] = new_metric(state, Counter)
            value = state["state"]
            print(f"{name} -> {value}")
            counters[name]._value.set(value)
    
        print("Processing gauges...")
        for name in GAUGE_NAMES:
            state = fetch_entity_state(name)
            if name not in gauges:
                gauges[name] = new_metric(state, Gauge)
            value = state["state"]
            print(f"{name} -> {value}")
            gauges[name].set(value)

        print(f"Done, sleeping for {SCRAPE_INTERVAL}s.")
        sleep(SCRAPE_INTERVAL)
