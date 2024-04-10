"""Command-line functions / entry points."""

import sys
from time import sleep

import click
from loguru import logger as log
from prometheus_client import start_http_server, Info, Counter, Gauge

from . import __version__
from .config import load_config_file
from .collector import new_metric, fetch_entity_state


def configure_logging(verbose: int):
    """Configure loguru logging / change log level.

    Parameters
    ----------
    verbose : int
        The desired log level, 0=WARNING (do not change the logger config),
        1=INFO, 2=DEBUG, 3=TRACE. Higher values will map to TRACE.
    """
    level = "WARNING"
    if verbose == 1:
        level = "INFO"
    elif verbose == 2:
        level = "DEBUG"
    elif verbose >= 3:
        level = "TRACE"
    # set up logging, loguru requires us to remove the default handler and
    # re-add a new one with the desired log-level:
    log.remove()
    log.add(sys.stderr, level=level)
    log.info(f"Set logging level to [{level}] ({verbose}).")


def prepare_export(config):
    log.debug(config)
    start_http_server(port=config.listen.port, addr=config.listen.addr)
    info = Info(
        name=f"{config.metric_pfx}_collector",
        documentation="SUN2000 inverter series metrics collector (via HomeAssistant)",
    )
    info.info(
        {
            "version": __version__,
            "collection_interval": f"{config.scrape_interval}s",
        }
    )

    log.success(
        f"{__package__} {__version__} started, "
        f"collection interval {config.scrape_interval}s."
    )
    log.success(f"Providing metrics via HTTP on port {config.listen.port}.")


@click.command(help="Run the HomeAssistant-SUN2K metrics exporter.")
@click.option("--config", type=str, help="A YAML configuration file.")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase logging verbosity, may be repeated up to 3 times.",
)
@click.version_option()
def run_exporter(verbose, config):
    """Main CLI entry point for the HA-SUN2K exporter. Blocking.

    Parameters
    ----------
    verbose : int
        Verbosity level for logging, ranges from 0 ("WARNING") to 3 ("TRACE").
    config : str
        A path to a configuration file.
    """
    # do a first logging configuration to respect the command line parameters:
    configure_logging(verbose)

    config = load_config_file(config)

    # verbosity might have been specified in the config / environment:
    if config.verbosity > verbose:
        configure_logging(config.verbosity)

    prepare_export(config)

    counters = {}
    gauges = {}

    while True:
        print("Updating metrics...")

        print("Processing counters...")
        for name in config.counters:
            value = 0
            try:
                state = fetch_entity_state(name, config)
                value = state["state"]
                print(f"{name} -> {value}")
            except:
                log.error(f"ERROR: fetching [{name}] failed, setting to -> {value}")
            if name not in counters:
                counters[name] = new_metric(state, Counter, config)
            counters[name]._value.set(value)

        print("Processing gauges...")
        for name in config.gauges:
            value = 0
            try:
                state = fetch_entity_state(name, config)
                value = state["state"]
                print(f"{name} -> {value}")
            except:
                log.error(f"ERROR: fetching [{name}] failed, setting to -> {value}")
            if name not in gauges:
                gauges[name] = new_metric(state, Gauge, config)
            gauges[name].set(value)

        print(f"Done, sleeping for {config.scrape_interval}s.")
        sleep(config.scrape_interval)
