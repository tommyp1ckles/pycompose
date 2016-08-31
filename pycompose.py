from compose.cli.main import setup_logging, TopLevelCommand, parse_doc_section, \
    perform_command, setup_console_handler
from compose.cli.utils import get_version_info
from inspect import getdoc

import compose.cli.docopt_command as dp
import functools
import logging
import sys

console_handler = logging.StreamHandler(sys.stderr)

def apiDispatch(args):
    """
    Does the same thing as the dispatch function in compose.cli.main.py but instead
    of using os.argv it uses a the passed args array. Also does not catch any
    exceptions so they can be caught programatically.
    params:
        args: Array of argument strings.
    """
    setup_logging()
    dispatcher = dp.DocoptDispatcher(
        TopLevelCommand,
        {'options_first': True, 'version': get_version_info('compose')})
    # Don't handle argument exceptions here, let them be caught outside of the apiDispatch.
    options, handler, command_options = dispatcher.parse(args)
    setup_console_handler(console_handler, options.get('--verbose'))
    return functools.partial(perform_command, options, handler, command_options)

def up(filename=None):
    """
    Runs the equivilant of a docker-compose up command.
    """
    opts = ["up"]
    if filename != None:
        opts.append("-f")
        opts.append(filename)
    apiDispatch(opts)()

def down(rmi=None, volumes=False, removeOrphans=False):
    """
    Runs the equivilant of a doker-compose down command.
    """
    opts = ["down"]
    if rmi != None:
        opts.append("--rmi")
        opts.append(rmi)
    if volumes:
        opts.append("--volumes")
    if removeOrphans:
        opts.append("--remove-orphans")
    apiDispatch(opts)()

def build(noCache=False, pull=False, forceRm=False):
    """
    Runs the equivilant of a docker-compose build command
    """
    opts = ["build"]
    if noCache:
        opts.append("--no-cache")
    if pull:
        opts.append("--pull")
    if forceRm:
        opts.append("--force-rm")
    apiDispatch(opts)()

