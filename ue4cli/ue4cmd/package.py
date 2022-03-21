#!/usr/bin/env python

import os
import sys
import argparse
from distutils.util import strtobool

from stdout import * 

from ue4sys import path as ue4path
from ue4cmd import common as ue4common

with_bv = True

def func(args, remainder):
	# -------------------------------------- make command string
	execute = str()
	arguments = list()

	execute = '%s BuildCookRun' % ue4path.get_engine_directories()['runuat']

	arguments.append('-project=%s' % ue4path.get_project_directories()['uproject'])

	if args.skipbuild:
		arguments.append('-skipbuild') 
	else:
		arguments.append('-build') 
		if args.type == 'client':
			arguments.append('-platform=%s' % args.platform)
			arguments.append('-clientconfig=%s' % args.config)

		if args.type == 'server':
			arguments.append('-server')
			arguments.append('-serverplatform=%s' % args.platform)
			arguments.append('-serverclientconfig=%s' % args.config)

		if args.type == 'all':
			arguments.append('-platform=%s' % args.clientplatform)
			arguments.append('-clientconfig=%s' % args.clientconfig)
			arguments.append('-server')
			arguments.append('-serverplatform=%s' % args.clientplatform)
			arguments.append('-serverclientconfig=%s' % args.clientconfig)

	if args.archive:
		arguments.append('-archive')
		arguments.append('-archivedirectory=%s' % args.archivedirectory)

	if args.stage:
		arguments.append('-stage')
		arguments.append('-stagingdirectory=%s' % args.stage)
		arguments.append('-nodebuginfo')
	else:
		arguments.append('-skipstage')

	if args.map:
		arguments.append('-map=%s' % args.map)

	if not args.skipcook:
		arguments.append('-cook') 
		arguments.append('-iterate') 
		arguments.append('-compressed') 

	if not args.nopak:
		arguments.append('-pak')
		if with_bv:
			arguments.append('-bvpak')

	arguments.append('-nop4') 
	arguments.append('-fileopenlog')
	arguments.append('-utf8output')

	if remainder:
		arguments.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	command = ue4common.get_command(execute, arguments)


plaforms = ['win64', 'win32', 'mac', 'linux']
configurations = ['debug', 'debuggame', 'development', 'shipping', 'test']
def add_parser(sub_parser):
	if not ue4path.is_engine_directory_valid():
		error('Failed to get valid engine directory')
		return None

	return sub_parser.add_parser('package')

def add_argument(parser):
	# -------------------------------------- set arguments
	parser.add_argument('-type', 
		choices=['client', 'server', 'all'],
		type=str,
		metavar='{client|server|all}',
		required=True)

	if '-type=client' in sys.argv:
		parser.add_argument('-platform',
			type=str,
			choices=plaforms,
			default='win64',
			metavar='{%s}' % '|'.join(plaforms),
			required=False)

		parser.add_argument('-config',
			type=str,
			choices=configurations,
			default='development',
			metavar='{%s}' % '|'.join(configurations),
			required=False)	


	if '-type=server' in sys.argv:
		parser.add_argument('-platform',
			type=str,
			choices=plaforms,
			metavar='{%s}' % '|'.join(plaforms),
			default='win64',
			required=False)

		parser.add_argument('-config',
			type=str,
			choices=configurations,
			default='development',
			metavar='{%s}' % '|'.join(configurations),
			required=False)	

	if '-type=all' in sys.argv:
		parser.add_argument('-clientplatform',
			choices=plaforms,
			type=str,
			default='win64',
			metavar='{%s}' % '|'.join(plaforms),
			required=False)

		parser.add_argument('-clientconfig',
			choices=configurations,
			type=str,
			default='development',
			metavar='{%s}' % '|'.join(configurations),
			required=False)	

		parser.add_argument('-serverplatform',
			choices=plaforms,
			type=str,
			default='win64',
			metavar='{%s}' % '|'.join(plaforms),
			required=False)

		parser.add_argument('-serverconfig',
			choices=configurations,
			type=str,
			default='development',
			metavar='{%s}' % '|'.join(configurations),
			required=False)	

	parser.add_argument('-skipbuild', action='store_true')
	parser.add_argument('-skipcook', action='store_true')
	parser.add_argument('-nopak', action='store_true')

	parser.add_argument('-archive', action='store_true')
	if '-archive' in sys.argv:
		parser.add_argument('-archivedirectory',
			type=str,
			default='%s\\Archive' % ue4path.get_engine_directories()['saved_dir'],
			metavar='${archivedirectory}',
			required=False)

	parser.add_argument('-stage', action='store_true')
	if '-stage' in sys.argv:
		parser.add_argument('-stagedirectory',
			type=str,
			default='%s\\Stage' % ue4path.get_engine_directories()['saved_dir'],
			metavar='${stagedirectory}',
			required=False)

	parser.add_argument('-map', 
		type=str,
		metavar='\'${map1}+${map2}+...+${mapN}\'',
		required=False)

	parser.set_defaults(func=func);

	return parser
