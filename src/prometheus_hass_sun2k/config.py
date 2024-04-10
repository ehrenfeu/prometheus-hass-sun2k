"""Configuration loader function(s)."""

from box import Box


def load_config_file(filename):
    """Assemble a config object by loading values from a file."""
    config = Box.from_yaml(filename=filename)
    if "addr" not in config.listen.keys():
        config.listen.addr = "0.0.0.0"
    if "port" not in config.listen.keys():
        config.listen.port = 9177
    if "scrape_interval" not in config.keys():
        config.scrape_interval = 15
    if "metric_pfx" not in config.keys():
        config.metric_pfx = "sun2k"
    if "entity_pfx" not in config.keys():
        config.entity_pfx = "sensor.inverter"
    if "counters" not in config.keys():
        config.counters = [
            "total_yield",
            "daily_yield",
        ]
    if "gauges" not in config.keys():
        config.counters = [
            "input_power",
            "day_active_power_peak",
            "active_power",
            "reactive_power",
            "power_factor",
            "efficiency",
            "internal_temperature",
        ]
    if "verbosity" not in config.keys():
        config.verbosity = 0
    return config
