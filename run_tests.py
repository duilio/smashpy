#!/usr/bin/env python
"""Main entry point"""

# copied directly from 2.7's unittest/__main__.py b/c coverage can't do -m

import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'tests'))

if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m unittest"

# autodiscover if no params are given
if len(sys.argv) == 1:
    sys.argv.append('discover')

__unittest = True

from unittest.main import main, TestProgram, USAGE_AS_MAIN
TestProgram.USAGE = USAGE_AS_MAIN

import logging

loglevel = os.environ.get('DEBUG', 'FATAL')
if loglevel not in ('NOTSET', 'DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR',
                    'CRITICAL', 'FATAL'):
    from warnings import warn
    warn('Environment variable DEBUG set with an unknown debug level. '
         'Default to FATAL.')
    loglevel = 'FATAL'

loglevel = getattr(logging, loglevel)
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=loglevel)

os.chdir('tests')
main(module=None)
