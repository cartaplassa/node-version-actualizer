#!/usr/bin/env python3
"""
Simple IO boilerplate. Your description goes here.

Args:
    filepath: Path to the Markdown file.
"""

__author__ = "Cartaplassa"
__version__ = "1.0.0"
__license__ = "GPL-3.0"

import argparse
import os
import logging
from datetime import datetime
from pathlib import PurePath

path = PurePath()

def setup_argparse():
    parser = argparse.ArgumentParser()
    # Required positional arguments
    parser.add_argument(
        "number",
        type=int,
        help="Some number"
    )
    parser.add_argument(
        "date",
        type=str,
        help="Some date, eg. 01.01.2025"
    )
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    parser.add_argument(
        "-f", "--format",
        type=str,
        help="Datetime format (1989 C standard-compliant)",
        default="%d.%m.%Y"
    )
    # Defaulted IO arguments
    parser.add_argument(
        "-i", "--input", 
        type=str,
        help="Path to input table",
        default="./res/input.txt"
    )
    parser.add_argument(
        "-o", "--output", 
        type=str,
        help="Path to output folder",
        default="./res/output.txt"
    )
    # Optional verbosity
    parser.add_argument(
        "-v", "--verbosity",
        action="count",
        help="Set verbosity level"
    )
    # Specify output of "--version"
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s (version {__version__})"
    )
    return parser.parse_args()

logging.getLogger().setLevel(logging.NOTSET)
logger = logging.getLogger()
FILE_HANDLER_FMT = (
    "%(asctime)s-%(msecs)04d [%(levelname)s]"
    "(%(name)s:%(funcName)s:%(lineno)d): %(message)s"
)
FILE_DATE_FMT = '%Y-%m%d-%H%M%S'
CLI_HANDLER_FMT = (
    "%(asctime)s-%(msecs)04d [%(levelname)s]"
    "(%(name)s): %(message)s"
)
CLI_DATE_FMT = "%H%M%S"

def setup_logger(args):
    if not os.path.exists('logs'): os.mkdir('logs')

    file_handler = logging.FileHandler(
        "logs/debug-" + datetime.strftime(
            datetime.now(), FILE_DATE_FMT
        ) + ".log"
    )
    file_handler.setFormatter(logging.Formatter(
        fmt=FILE_HANDLER_FMT,
        datefmt=FILE_DATE_FMT
    ))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    cli_handler = logging.StreamHandler()
    cli_handler.setLevel(logging.CRITICAL)
    cli_handler.setFormatter(logging.Formatter(
        fmt=CLI_HANDLER_FMT,
        datefmt=CLI_DATE_FMT
    ))
    logger.addHandler(cli_handler)

    if not args.verbosity:
        cli_handler.setLevel(logging.ERROR)
    elif args.verbosity == 1:
        cli_handler.setLevel(logging.WARNING)
    elif args.verbosity == 2:
        cli_handler.setLevel(logging.INFO)
    elif args.verbosity >= 3:
        cli_handler.setLevel(logging.DEBUG)
    else:
        logger.critical("Negative verbosity count")
    logger.debug(f"Logger set up with {cli_handler.level} level")


def main(args):
    try:
        with open(args.input, 'r', encoding='utf-8') as input_fs:
            content = input_fs.read()
        logger.debug("Input read")
        parsed_date = datetime.strptime(args.date, args.format)
        logger.debug("Parsed date: " + datetime.strftime(parsed_date, "%Y-%m-%d"))
        formatted_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        logger.debug("Date formatted")
        new_content = content + f'\n{formatted_date} - {args.number}\nEnd'
        with open(args.output, 'w', encoding='utf-8') as output_fs: # save as UTF-8
            output_fs.write(new_content)

    except FileNotFoundError:
        logger.critical(f"File not found at {args.input}")
    except Exception as e:
        logger.critical(f"An error occurred: {e}")



if __name__ == "__main__":
    args = setup_argparse()
    setup_logger(args)
    main(args)



