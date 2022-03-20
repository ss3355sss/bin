#!/usr/bin/env python

import os
import sys
import argparse
from distutils.util import strtobool

from stdout import * 

from ue4sys import path as ue4path
from ue4cmd import common as ue4common

def func(args, remainder):
	execute = str()
	arguments = list()
	# -------------------------------------- make command string
	execute = ue4common.get_gameplay_execute(args, is_server=False)
	if not execute:
		return

	arguments.append('%s' % args.map)
	
	arguments.extend(ue4common.get_gameplay_options(args, is_server=False))
	arguments.extend(ue4common.get_log_options(args))
	
	if remainder:
		arguments.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	command = ue4common.get_command(execute, arguments)

def add_parser(sub_parser):
	return sub_parser.add_parser('game')

def add_argument(parser):
	ue4common.add_gameplay_execute_argument(parser)

	parser.add_argument(
		'-map',
		required = False,
		default='DefaultStartMap',
		metavar='${map}')

	ue4common.add_gameplay_options_argument(parser)	
	ue4common.add_log_options_argument(parser)

	# -------------------------------------- set func
	parser.set_defaults(func=func);


