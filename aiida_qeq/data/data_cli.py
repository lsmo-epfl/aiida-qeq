from __future__ import absolute_import
import sys
import click
from aiida.cmdline.commands import cmd_data
from aiida.cmdline.utils import decorators


# See aiida.cmdline.data entry point in setup.json
@cmd_data.group('qeq')
def cli():
    """Command line interface for aiida-qeq"""
    pass


@cli.command('list')
@decorators.with_dbenv
def list_():  # pylint: disable=redefined-builtin
    """
    Display all DiffParameters nodes
    """
    from aiida.orm.querybuilder import QueryBuilder
    from aiida.plugins import DataFactory
    DiffParameters = DataFactory('qeq')

    qb = QueryBuilder()
    qb.append(DiffParameters)
    results = qb.all()

    s = ""
    for result in results:
        obj = result[0]
        s += "{}, pk: {}\n".format(str(obj), obj.pk)
    sys.stdout.write(s)


@cli.command('export')
@click.option(
    '--outfile',
    '-o',
    type=click.Path(dir_okay=False),
    help='Write output to file (default: print to stdout).')
@click.argument('pk', type=int)
@decorators.with_dbenv
def export(outfile, pk):
    """Export a DiffParameters node, identified by PK, to plain text"""
    from aiida.orm import load_node
    node = load_node(pk)
    string = str(node)

    if outfile:
        with open(outfile, 'w') as f:
            f.write(string)
    else:
        click.echo(string)
