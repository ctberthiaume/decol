import click
import csv
import os
import sys
from operator import itemgetter


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class Columns(click.ParamType):
    name = 'columns'

    def convert(self, value, param, ctx):
        if ctx.obj and 'headers' in ctx.obj:
            self.fail('may not be used with --headers', param, ctx)
        else:
            columns = []
            try:
                for item in value.split(','):
                    if item.find(':') != -1:
                        range_parts = item.split(':')
                        if len(range_parts) != 2:
                            self.fail('column range must be in the form INT:INT.', param, ctx)
                        # Range here is [int, int], inclusive on both sides.
                        # Different from Python convention of [int, int).
                        columns.extend(list(range(int(range_parts[0]), int(range_parts[1]) + 1)))
                    else:
                        columns.append(int(item))
            except ValueError:
                self.fail('only integers are permitted as column indexes.', param, ctx)
            for c in columns:
                if c == 0:
                    self.fail('%i is not a valid column index.' % c, param, ctx)
            if ctx.obj:
                ctx.obj['columns'] = columns
            else:
                ctx.obj = { 'columns': columns }
            return columns


class Headers(click.ParamType):
    name = 'headers'

    def convert(self, value, param, ctx):
        if ctx.obj and 'columns' in ctx.obj:
            self.fail('may not be used with --columns', param, ctx)
        else:
            headers = value.split(',')
            if ctx.obj:
                ctx.obj['headers'] = headers
            else:
                ctx.obj = { 'headers': headers }
            return headers


class Separator(click.ParamType):
    name = 'separator'

    def convert(self, value, param, ctx):
        return value.encode('utf-8').decode('unicode_escape')


def dslice(x, indexes):
    """Slice with discontinuous indexes"""
    if not x or not indexes:
        return []
    subx = itemgetter(*indexes)(x)
    if len(indexes) == 1:
        return [subx]
    else:
        return list(subx)


def spaces(text):
    """Replace all whitespace with single spaces"""
    return ' '.join(text.split())


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--columns', type=Columns(),
              help=spaces("""Comma-separated list of 1-based column indexes to
              remove. Negative integers will index from the end. May use a
              range, e.g. 1:2 or -3:-2 for first and second of three columns.
              Ranges must always be given in left to right column order for both
              positive and negative indexes. Mutually exclusive with
              --headers."""))
@click.option('-H', '--headers', type=Headers(),
              help=spaces("""Comma-separated list of columns to remove by
              first-line header. Mutually exclusive with --columns."""))
@click.option('-s', '--sep', default=',', type=Separator(), show_default=True,
              help='Column separator.')
@click.option('-o', '--output-sep', type=Separator(),
              help='Output column separator. [default: --sep value]')
@click.option('--keep', is_flag=True, show_default=True,
              help=spaces("""Keep only the specified columns in the order
              specified in --columns or --headers."""))
@click.argument('input', type=click.File())
@click.argument('output', type=click.File(mode='w', atomic=True))
@click.version_option()
def cli(columns, headers, sep, output_sep, keep, input, output):
    """A tool to delete columns from a CSV file."""
    reader = csv.reader(input, delimiter=str(sep))
    try:
        header_fields = next(reader)
    except StopIteration:
        return

    colnum = len(header_fields)
    columns0 = []

    if headers:
        header_lookup = dict((h, i) for i, h in enumerate(header_fields))
        for h in headers:
            try:
                columns0.append(header_lookup[h])
            except KeyError:
                pass
    elif columns:
        # column indexes come from user as 1-based
        # - convert to 0-based indexing
        # - adjust negative indices
        # - check range
        for c in columns:
            if c > 0 and c <= colnum:
                columns0.append(c - 1)
            elif c < 0 and c >= -colnum:
                columns0.append(c + colnum)
        columns0 = [c for c in columns0 if c < colnum]

    if not keep:
        columnsi = list(range(colnum))
        columns0 = [i for i in columnsi if i not in columns0]

    if columns0:
        if output_sep is None:
            output_sep = sep
        writer = csv.writer(output, delimiter=str(output_sep), lineterminator=os.linesep)
        writer.writerow(dslice(header_fields, columns0))
        for row in reader:
            writer.writerow(dslice(row, columns0))
