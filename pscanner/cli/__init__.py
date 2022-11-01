# SPDX-FileCopyrightText: 2022-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import click
from pscanner import is_port_open, is_subnet, hosts_in_subnet, is_host_alive
from ..__about__ import __version__


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name='pscanner')
@click.argument('host')
@click.argument('port')
@click.pass_context
def pscanner(ctx: click.Context, host, port):
    if is_subnet(host):
        for ip in hosts_in_subnet(host):
            if is_host_alive(str(ip)):
                is_port_open(str(ip), port)
    else:       
        if is_host_alive(host):     
            is_port_open(host, port)