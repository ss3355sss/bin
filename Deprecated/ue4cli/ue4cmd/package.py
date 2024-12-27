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
	params = list()
	options = list()

	execute = '%s BuildCookRun' % ue4path.get_engine_directories()['runuat']

	options.append('-project=%s' % ue4path.get_project_directories()['uproject'])

	if args.skipbuild:
		options.append('-skipbuild') 
	else:
		options.append('-build') 
	if args.type == 'client':
		options.append('-platform=%s' % args.platform)
		options.append('-clientconfig=%s' % args.config)

	if args.type == 'server':
		options.append('-server')
		options.append('-serverplatform=%s' % args.platform)
		options.append('-serverclientconfig=%s' % args.config)

	if args.type == 'all':
		options.append('-platform=%s' % args.clientplatform)
		options.append('-clientconfig=%s' % args.clientconfig)
		options.append('-server')
		options.append('-serverplatform=%s' % args.clientplatform)
		options.append('-serverclientconfig=%s' % args.clientconfig)

	if args.archive:
		options.append('-archive')
		options.append('-archivedirectory=%s' % args.archivedirectory)
		options.append('-stage')
		options.append('-nodebuginfo')

	if args.stage:
		options.append('-stage')
		options.append('-nodebuginfo')

	if args.stagedirectory:
		options.append('-stagingdirectory=%s' % args.stagedirectory)

	if args.skipstage:
		options.append('-skipstage')

	if args.map:
		options.append('-map=%s' % args.map)

	if not args.skipcook:
		options.append('-cook') 
		options.append('-iterate') 
		options.append('-compressed') 

	if not args.skippak:
		options.append('-pak')
		if with_bv:
			options.append('-bvpak')

	if ue4path.is_exist(args.ddc):
		options.append('-ddc=%s' % args.ddc)
	else:
		options.append('-ddc=noshared')

	options.append('-nop4') 
	options.append('-fileopenlog')
	options.append('-utf8output')

	options.extend(ue4common.get_log_options(args))

	if remainder:
		options.extend(ue4common.get_remainder(remainder))

	# -------------------------------------- exec command
	ue4common.exec_command(execute, params, options)


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
	parser.add_argument('-skipstage', action='store_true')
	parser.add_argument('-skippak', action='store_true')

	parser.add_argument('-archive', action='store_true')
	if '-archive' in sys.argv:
		parser.add_argument('-archivedirectory',
			type=str,
			default='%s\\Archive' % ue4path.get_project_directories()['saved_dir'],
			metavar='${archivedirectory}',
			required=False)

	parser.add_argument('-stage', action='store_true')
	parser.add_argument('-stagedirectory',
		type=str,
		#default='%s\\Stage' % ue4path.get_project_directories()['saved_dir'],
		metavar='${stagedirectory}',
		required=False)

	parser.add_argument('-map', 
		type=str,
		metavar='\'${map1}+${map2}+...+${mapN}\'',
		required=False)

	parser.add_argument(
		'-ddc',
		type=str,
		default='',
		metavar='${path}')

	ue4common.add_log_options_argument(parser)

	parser.set_defaults(func=func);

	return parser
