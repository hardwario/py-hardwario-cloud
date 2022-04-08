import logging
import click
from . import codec
from ..api import Api, DEFAULT_API_URL

logger = logging.getLogger(__name__)


@click.group(name='cloud', help='Commands for CLOUD.')
@click.option('--url', metavar='URL', default=DEFAULT_API_URL, show_default=True, required=True)
@click.option('--token', metavar='TOKEN', required=True)
@click.pass_context
def cli(ctx, url, token):
    ctx.obj['api'] = Api(url, token=token)


cli.add_command(codec.cli)


def main():
    cli(obj={}, auto_envvar_prefix='HARDWARIO_CLOUD')
