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
	execute, params, options = ue4common.get_gameplay_execute(args, is_server=False)
	if not execute:
		return
	target = str()
	if args.target == 'editor':
		target = 'Editor'
	if args.target == 'client':
		target = ''
	if args.target == 'server':
		target = 'Server'

	params.append('%s%s' % (ue4path.get_project(), target))
	params.append('%s' % args.platform)
	params.append('%s' % args.config)
	params.append('%s' % ue4path.get_project_directories()['uproject'])

	options.append('-waitMutex') 
	options.append('-NoHotReload') 

	if remainder:
		options.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	ue4common.exec_command(execute, params, options)


targets = ['editor', 'client', 'server']
platforms = ['win64', 'win32', 'mac', 'linux']
configurations = ['debug', 'debuggame', 'development', 'shipping', 'test']
def add_parser(sub_parser):
	if not ue4path.is_engine_directory_valid():
		error('Failed to get valid engine directory')
		return None

	return sub_parser.add_parser('build')

def add_argument(parser):
	# -------------------------------------- set arguments
	parser.add_argument('-target', 
		type=str,
		choices=targets,
		default='editor',
		metavar='{%s}' % '|'.join(targets),
		required=False)

	parser.add_argument('-platform',
		type=str,
		choices=platforms,
		default='win64',
		metavar='{%s}' % '|'.join(platforms),
		required=False)

	parser.add_argument('-config',
		type=str,
		choices=configurations,
		default='development',
		metavar='{%s}' % '|'.join(configurations),
		required=False)	


	parser.set_defaults(func=func);

