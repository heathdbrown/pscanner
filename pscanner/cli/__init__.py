# SPDX-FileCopyrightText: 2022-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import asyncio
import click
import logging
from pscanner import (
    are_alive,
    is_port_open,
    is_subnet,
    hosts_in_subnet,
    is_host_alive,
    is_port_range,
    ports_from_range,
    port_scan,
)
from ..__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="pscanner")
@click.option("-v", "--verbose", count=True)
@click.argument("host")
@click.argument("port")
@click.pass_context
def pscanner(ctx: click.Context, host, port, verbose):
    if not verbose:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level="INFO"
        )
    else:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level="DEBUG"
        )
    if is_subnet(host):
        hosts = hosts_in_subnet(host)
        logging.info("pinging %s hosts" % len(hosts))
        alive_hosts = are_alive(hosts)
        logging.info("found %s alive" % len(alive_hosts))
        for ip in alive_hosts:
            if is_port_range(port):
                port_scan(str(ip), ports_from_range(port))
            else:
                is_port_open(str(ip), port)
    else:
        if is_host_alive(host):
            if is_port_range(port):
                port_scan(host, ports_from_range(port))
            else:
                is_port_open(host, port)
