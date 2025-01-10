#!/usr/bin/env python

import os
import sys
import argparse
from distutils.util import strtobool

from stdout import * 

from ue4sys import path as ue4path
from ue4cmd import common as ue4common

def func(args, remainder):
	# -------------------------------------- make command string
	execute, params, options = ue4common.get_gameplay_execute(args, is_server=True)
	if not execute:
		return

	params.append('%s' % args.map)
	
	options.extend(ue4common.get_additional_gameplay_options(args, is_server=True))
	options.extend(ue4common.get_log_options(args))
	
	if remainder:
		options.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	ue4common.exec_command(execute, params, options)

def add_parser(sub_parser):
	return sub_parser.add_parser('server')

def add_argument(parser):
	ue4common.add_gameplay_execute_argument(parser)

	parser.add_argument(
		'-map',
		required=False,
		default='DefaultStartMap',
		metavar='${map}')

	#parser.add_argument('-listen', action='store_true')
	
	ue4common.add_additional_gameplay_options_argument(parser)	
	ue4common.add_log_options_argument(parser)

	# -------------------------------------- set func
	parser.set_defaults(func=func);


