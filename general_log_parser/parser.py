#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, traceback, codecs, os, re, errno, click
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from general_log_parser import __version__
from general_log_parser import __executable__

is_python_2 = sys.version_info[0] == 2

import logging
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.ERROR)

import fn
from fn import F

split = None
strip = None

if is_python_2:
    split = fn.iters.flip(unicode.split)
    strip = fn.iters.partial(fn.iters.flip(unicode.rstrip), '\r\n')
else:
    split = fn.iters.flip(str.split)
    strip = fn.iters.partial(fn.iters.flip(str.rstrip), '\r\n')

def has_piped_input():
    return not sys.stdin.isatty()


def print_last_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logger.error("Exception occured:")
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)


def is_valid_date(match_pattern, from_time, to_time, f):
    if from_time == None or to_time == None:
        return True

    match = match_pattern.match(f)
    if not match:
        return False

    date = match.group(1)
    return from_time <= date and to_time >= date


def gen_find(log, from_time, to_time, input_dir):
    if from_time == None or to_time == None:
        return [log]

    FILE_REGEX = re.compile(log.replace("{}", "(\d*)"))

    func = F() >> os.walk \
            >> (fn.iters.map, lambda s: dict(path=s[0], filelist=(n for n in s[2]))) \
            >> (fn.iters.map, lambda d: dict(path=d['path'], filelist=fn.iters.filter(fn.iters.partial(is_valid_date, FILE_REGEX, from_time, to_time), d['filelist']))) \
            >> (fn.iters.map, lambda d: fn.iters.map(fn.iters.partial(os.path.join, d['path']), d['filelist'])) \
            >> chain_sources

    return func(input_dir)


def gen_open(filenames):
    for name in filenames:
        with codecs.open(name, 'r', 'utf-8') as f:
            yield f


def chain_sources(sources):
    for s in sources:
        for item in s:
            yield item


def filter_regex(line_filters, lines):
    if not line_filters:
        for line in lines:
            yield line
        return

    for line in lines:
        for line_filter in line_filters:
            if line_filter.search(line):
                yield line
                break


def filter_negative_regex(line_filters, lines):
    if not line_filters:
        for line in lines:
            yield line
        return

    for line in lines:
        for line_filter in line_filters:
            if line_filter.search(line):
                break
        else:
            yield line


def filter_conditions(cond_filters, lines):
    if not cond_filters:
        for line in lines:
            yield line
        return

    for line in lines:
        for cond_filter in cond_filters:
            if eval(cond_filter.format(*line)):
                yield line
                break


def print_lines(out_format, lines):
    for line in lines:
        if out_format:
            click.echo(out_format.format(*line))
        else:
            click.echo('\t'.join(line))


def parse_log(args):
    from_time    = args['from']
    to_time      = args['to']
    log_name     = args['log']
    input_dir    = args['input_dir']
    line_filters = list(map(lambda x: re.compile(x, re.IGNORECASE), args['line_filter']))
    not_line_filters = list(map(lambda x: re.compile(x, re.IGNORECASE), args['not_line_filter']))
    cond_filters = args['cond_filter']
    out_format   = args['out_format'].replace('\\t', '\t') if args['out_format'] else None
    field_sep    = args['field_sep'].replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r') if args['field_sep'] else '\t'

    gen_input = None
    if has_piped_input():
        gen_input = F(read_from_stdin)
    else:
        gen_input = F(gen_find, log_name, from_time, to_time, input_dir) >> gen_open >> chain_sources

    func =  gen_input \
            >>  (filter_regex, line_filters) \
            >>  (filter_negative_regex, not_line_filters) \
            >> (map, strip) \
            >> (map, fn.iters.partial(split, field_sep)) \
            >> (filter_conditions, cond_filters) \
            >> (print_lines, out_format)
    func()


def read_from_stdin():
    while True:
        line = sys.stdin.readline()
        if line:
            if is_python_2:
                yield unicode(line, "utf-8")
            else:
                yield line
        else:
            break


def validate_args(kwargs):
    if not has_piped_input():
        if not kwargs.get('log'):
            return { 'err' : True, 'messages' : ['Please specify log file or pipe input from another source'] }

    return { 'err' : False }

CONTEXT_SETTINGS = dict(
    max_content_width=100
)

class MyCLI(click.Command):
    def format_usage(self, ctx, formatter):
        indents = 17
        usage_text = [
            "",
            "Usage: %s --log=LOG --input-dir=INPUT_DIR" % (__executable__),
            " " * indents + "--from=FROM_TIME --to=TO_TIME",
            " " * indents + "[--line-filter=LINE_FILTER...]",
            " " * indents + "[--cond-filter=COND_FILTER...]",
            " " * indents + "[--out-format=OUT_FORMAT]",
            " " * indents + "[--field-sep=FIELD_SEP]",
            " " * indents + "[-v --verbose]",
            "       %s [--version]" % (__executable__),
            "       cat input_file | %s [OPTIONS]" % (__executable__),
            ""
        ]
        formatter.write('\n'.join(usage_text))


@click.command(cls=MyCLI, name="parser", context_settings=CONTEXT_SETTINGS, short_help="short", help="Parse a log file or piped input line by line based on specific patterns. If there's piped input then we don't have to specify --log option.")
@click.option('-l', '--log', metavar="LOG", help="Name of the log. It could also be a pattern that has a time part in the form of YYYYMMDD, e.g  game.battle_pvp.log.{}, then the {} part will be replaced by the date specified by --from and --to.                                               \nE.g.  \nlogparser -l {}.log --from 20150401 --to 20150402             \nwill match 20150401.log and 20150402.log")
@click.option('-i', '--input-dir', metavar="INPUT_DIR", default=".", show_default=True, help="Name of the directory containing the logs. This should be specified correctly when --log use a time pattern.")
@click.option('--from', metavar="FROM_TIME", help="Start time of the logs. E.g 20140405")
@click.option('--to', metavar="TO_TIME", help="To time of the log. E.g 20140405")
@click.option('--line-filter', metavar="LINE_FILTER", multiple=True, help='One or more line filters using regex. To be executed before COND_FILTER. \n  E.g. --line-filter="mw001" --line-filter="mw002"  \nThis is a OR condition, i.e. any line that satisfies one filter will be counted.')
@click.option('--not-line-filter', metavar="NOT_LINE_FILTER", multiple=True, help='One or more negative line filters using regex. Line that contains this expression will be filtered out.')
@click.option('--cond-filter', metavar="COND_FILTER", multiple=True, help='One or more condition filters. This will be evaluated to python code so it will be slow!!! \n  E.g. "{1} > 23:56:13".                   \nThis is a OR condition, i.e. any line that satisfy one filter will be counted.')
@click.option('-f', '--field-sep', metavar="FIELD_SEP", help='Field separator in the input file. If nothing is specified tab will be used')
@click.option('-o', '--out-format', metavar="OUT_FORMAT", help='Output format. \n  E.g. "{} {} {} {}" or "{0} {1} {2}".           \nIf no ouput format is specified, the whole line is printed')
@click.option('-v', '--verbose', is_flag=True, default=False, help="Show verbose debug information")
@click.version_option(version=__version__, prog_name="General Log Parser",  help="Print version information")
@click.help_option('-h', '--help')
def main(*args, **kwargs):
    try:
        if kwargs['verbose']:
            logger.setLevel(logging.DEBUG)
            logger.debug(("Starting ...", kwargs))

        res = validate_args(kwargs)
        if res.get('err'):
            for message in res['messages']:
                click.echo(message)
                click.echo('Use %s -h for more information' % (__executable__))
        else:
            parse_log(kwargs)

        sys.stdout.flush()
    except Exception:
        print_last_exception()
        sys.exit(errno.EACCES)

if __name__ == '__main__':
    main()
