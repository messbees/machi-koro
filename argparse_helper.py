import argparse
import getpass
import logging
from colorlog import ColoredFormatter

def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog
def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')
    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=('Evolution Cli Client v0.0'),
        help='Version')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        parents=[parent_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(title='subcommands', dest='command')
    add_room_new_parser(subparsers, parent_parser)
    add_room_connect_parser(subparsers, parent_parser)
    add_room_start_parser(subparsers, parent_parser)
    add_room_update_parser(subparsers, parent_parser)
    add_update_parser(subparsers, parent_parser)
    return parser

def add_room_new_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'room_new',
        parents=[parent_parser],
        description='Creates new room',
        help='Creates new room')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')

def add_room_connect_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'room_connect',
        parents=[parent_parser],
        description='Connects to existing room',
        help='Connects to existing room')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')

def add_room_start_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'room_start',
        parents=[parent_parser],
        description='Starts the game',
        help='Starts the game')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')

def add_room_update_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'room_update',
        parents=[parent_parser],
        description='Update the room',
        help='Update the room')
    parser.add_argument(
        'name',
        type=str,
        help='Room name')

def add_update_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'update',
        parents=[parent_parser],
        description='Updates current state of the game',
        help='Updates current state of the game')
    parser.add_argument(
        'id',
        type=int,
        help='Game ID')
