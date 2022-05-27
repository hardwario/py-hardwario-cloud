import yaml
import click
import json
import sys
from loguru import logger


@click.group(name='message')
def cli():
    '''Message commands.'''


@cli.command('list')
@click.option('--device-id', metavar="DEVICE_ID")
@click.option('--group-id', metavar="GROUP_ID")
@click.option('--limit', type=click.IntRange(0, 100, clamp=True))
@click.option('--since', type=str)
@click.option('--before', type=str)
@click.option('--format', type=click.Choice(['json', 'yaml']), default='json', show_default=True)
@click.pass_context
def command_list(ctx, device_id, group_id, limit, since, before, format):
    '''List of messages.'''
    if not device_id and not group_id:
        raise click.UsageError('Missing option \'--device-id\' or \'--group-id\'')

    items = ctx.obj['api'].message_list(device_id=device_id, group_id=group_id, limit=limit, since=since, before=before)
    for item in items:
        if format == 'json':
            click.echo(json.dumps(item))
        else:
            click.echo(yaml.dump(item))
