import sys
import click
from loguru import logger
from . import codec
from ..api import Api, DEFAULT_API_URL


@click.group(name='cloud', help='Commands for CLOUD.')
@click.option('--url', metavar='URL', default=DEFAULT_API_URL, show_default=True, required=True)
@click.option('--token', metavar='TOKEN', required='--help' not in sys.argv)
@click.pass_context
def cli(ctx, url, token):
    ctx.obj['api'] = Api(url, token=token)


cli.add_command(codec.cli)


def main():
    cli(obj={}, auto_envvar_prefix='HARDWARIO_CLOUD')
