import yaml
import click
from loguru import logger


@click.group(name='codec')
def cli():
    '''Codec commands.'''


@cli.command('create')
@click.option('--name', required=True)
@click.pass_context
def command_create(ctx, name):
    '''Create new codec.'''
    resp = ctx.obj['api'].codec_create(name)
    click.echo(resp['id'])


@cli.command('upload')
@click.option('--id', metavar="ID", required=True)
@click.option('--name', type=str)
@click.option('--note', type=str)
@click.option('--decoder-type', type=click.Choice(['cbor', ' protobuf', 'javascript']), required=True)
@click.option('--decoder', type=click.File('r'), required=True)
@click.pass_context
def command_upload(ctx, id, name, note, decoder_type, decoder):
    '''Upload codec.'''
    decoder = decoder.read().strip()
    if decoder_type == 'cbor':
        try:
            yaml.safe_load(decoder)
        except Exception as e:
            raise Exception(f'Invalid JSON: {e}')
    resp = ctx.obj['api'].codec_update(id, name, note, decoder_type, decoder)
    click.echo('OK')


@cli.command('list')
@click.pass_context
def command_list(ctx):
    '''List of codec.'''
    codecs = ctx.obj['api'].codec_list(fields=['id', 'name', 'author_ids'])
    for codec in codecs:
        line = f'{codec["id"]} [authors: {len(codec["author_ids"])}] {codec["name"]}'.strip()
        click.echo(line)


@cli.command('show')
@click.option('--id', metavar="ID", show_default=True, required=True)
@click.pass_context
def command_list(ctx, id):
    '''Show codec detail.'''
    codec = ctx.obj['api'].codec_detail(id)
    click.echo(f'ID: {codec["id"]}')
    click.echo(f'Name: {codec["name"]}')
    click.echo(f'Created at: {codec["created_at"].replace("T", " ")}')
    click.echo(f'Updated at: {codec.get("updated_at", "").replace("T", " ")}')
    click.echo(f'Note: {codec.get("note", "")}')
    click.echo(f'Decoder type: {codec.get("decoder_type", "")}')
    click.echo(f'Decoder:')
    click.echo(codec.get("decoder", ""))


@cli.command('delete')
@click.option('--id', metavar="ID", required=True)
@click.confirmation_option(prompt='Are you sure you want to delete codec ?')
@click.pass_context
def command_delete(ctx, id):
    '''Delete codec.'''
    resp = ctx.obj['api'].codec_delete(id)
    click.echo('OK')


@cli.command('attach')
@click.option('--id', metavar="ID", required=True)
@click.option('--device-id', metavar="DEVICE_ID")
@click.option('--group-id', metavar="GROUP_ID")
@click.pass_context
def command_attach(ctx, id, device_id, group_id):
    '''Attach codec to group or device.'''
    if not device_id and not group_id:
        raise click.UsageError('Missing option \'--device-id\' or \'--group-id\'')

    if device_id:
        resp = ctx.obj['api'].codec_attach_to_device(id, device_id)
        if resp['codec_id'] != id:
            raise Exception('Save Error')
        click.echo('OK')

    if group_id:
        resp = ctx.obj['api'].codec_attach_to_group(id, group_id)
        if resp['codec_id'] != id:
            raise Exception('Save Error')
        click.echo('OK')


@cli.group(name='author')
def author():
    '''Autor commands.'''


@author.command('list')
@click.option('--id', metavar="ID", required=True)
@click.pass_context
def command_autor_list(ctx, id):
    '''List of authors.'''
    for author in ctx.obj['api'].codec_authors(id):
        click.echo(f'{author["id"]} <{author["email"]}> {author["name"]}')


@author.command('add')
@click.option('--id', metavar="ID", required=True)
@click.option('--author-id', metavar="ID", required=True)
@click.pass_context
def command_autor_add(ctx, id, author_id):
    '''Add author.'''
    for author in ctx.obj['api'].codec_author_add(id, author_id):
        click.echo(f'{author["id"]} <{author["email"]}> {author["name"]}')


@author.command('remove')
@click.option('--id', metavar="ID", required=True)
@click.option('--author-id', metavar="ID", required=True)
@click.pass_context
def command_autor_remove(ctx, id, author_id):
    '''Remove author.'''
    for author in ctx.obj['api'].codec_author_remove(id, author_id):
        click.echo(f'{author["id"]} <{author["email"]}> {author["name"]}')
