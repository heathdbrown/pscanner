# SPDX-FileCopyrightText: 2022-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import asyncio
import click
from pscanner import (
    are_alive,
    is_port_open,
    is_subnet,
    hosts_in_subnet,
    is_host_alive,
    is_port_range,
    ports_from_range,
)
from ..__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="pscanner")
@click.argument("host")
@click.argument("port")
@click.pass_context
def pscanner(ctx: click.Context, host, port):

    if is_subnet(host):
        hosts = hosts_in_subnet(host)
        print(f"pinging {len(hosts)} hosts")
        alive_hosts = are_alive(hosts)
        print(f"found {len(alive_hosts)} alive")
        for ip in alive_hosts:
            if is_port_range(port):
                for p in ports_from_range(port):
                    is_port_open(str(ip), p)
            else:
                is_port_open(str(ip), port)
    else:
        if is_host_alive(host):
            if is_port_range(port):
                for p in ports_from_range(port):
                    is_port_open(host, p)
            else:
                is_port_open(host, port)
