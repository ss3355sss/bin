#!/usr/bin/env python

import sys
import os

import argparse
from distutils.util import strtobool

from stdout import * 

from ue4sys import path as ue4path
from ue4cmd import common as ue4common


def func(args, remainder):
	# -------------------------------------- make command string
	execute, params, options = ue4common.get_gameplay_execute(args, is_server=False)
	if not execute:
		return

	if ue4path.is_exist(args.ddc):
		options.append('-ddc=%s' % args.ddc)
	else:
		options.append('-ddc=noshared')

	options.extend(ue4common.get_log_options(args))
	
	if remainder:
		options.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	ue4common.exec_command(execute, params, options)

def add_parser(sub_parser):
	if not ue4path.is_engine_directory_valid():
		error('Failed to get valid engine directory')
		return

	parser = sub_parser.add_parser('editor')
	return parser

def add_argument(parser):
	# -------------------------------------- set arguments
	parser.add_argument(
		'-ddc',
		type=str,
		#required=True,
		default='',
		metavar='${path}')

	ue4common.add_log_options_argument(parser)

	parser.set_defaults(func=func);

