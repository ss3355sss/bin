#!/usr/bin/env python

import os
import sys
import argparse

import datetime
from distutils.util import strtobool

from stdout import * 

from ue4sys import path as ue4path
from ue4cmd import common as ue4common

# -------------------------------------- handle command
def commonfunc(args, remainder):
	execute = str()
	arguments = list()
	# -------------------------------------- make command string
	execute = ue4common.get_gameplay_execute(args, is_server=False)
	if not execute:
		return

	if args.asrun == 'game':
		arguments.append('%s' % args.map)
	else:
		arguments.append('%s' % args.ip)

	arguments.extend(ue4common.get_gameplay_options(args, is_server=False))
	arguments.extend(ue4common.get_log_options(args))

	if not ue4path.is_exist(args.profileunit):
		error('Failed to get valid profileunit, %s' % args.profileunit)
		return None, None

	arguments.append('-profileunit=%s' % args.profileunit)

	if args.prefix:
		arguments.append('-prefix=%s' % args.prefix)
	if args.postfix:
		arguments.append('-postfix=%s' % args.postfix)
	if args.profiledir:
		arguments.append('-profilerdir=%s' % args.profiledir)

	if remainder:
		arguments.extend(ue4common.get_remainder(remainder))

	return execute, arguments;

def capturefunc(args, remainder):
	execute, arguments =  commonfunc(args, remainder)
	if not execute:
		return

	arguments.append('-capturetype=%s' % args.capturetype)
	if args.targetbuffers:
		arguments.append('-targetbuffers=%s' % args.targetbuffers)

	# -------------------------------------- exec command
	command = ue4common.get_command(execute, arguments)		

def memoryfunc(args, remainder):
	execute, arguments =  commonfunc(args, remainder)
	if not execute:
		return

	arguments.append('-dumpinterval=%s' % args.dumpinterval)

	# -------------------------------------- exec command
	command = ue4common.get_command(execute, arguments)		

def tracefunc(args, remainder):
	execute, arguments =  commonfunc(args, remainder)
	if not execute:
		return

	arguments.append('-profiler=%s' % args.profiler)

	# -------------------------------------- exec command
	command = ue4common.get_command(execute, arguments)		

def allfunc(args, remainder):
	display('#------------------------- profile capture')
	capturefunc(args, remainder)
	display('#------------------------- profile memory')
	memoryfunc(args, remainder)
	display('#------------------------- profile trace')
	tracefunc(args, remainder)

# -------------------------------------- add parser
def add_parser(sub_parser):
	return sub_parser.add_parser('profile')

# -------------------------------------- add arguments
def add_argument(parser):
	ue4common.add_gameplay_execute_argument(parser)

	parser.add_argument(
		'-asrun',
		type=str.lower,
		choices=['game', 'client'],
		metavar='{game|client}',
		required=True,
		)

	if '-asrun=game' in sys.argv:
		parser.add_argument(
			'-map',
			required=False,
			default='DefaultStartMap',
			metavar='${map}')

	if '-asrun=client' in sys.argv:
		parser.add_argument(
			'-ip',
			type=str,
			default='127.0.0.1',
			metavar='\'${server-ip}\'',
			required=False)

	parser.add_argument('-type', 
		choices=['capture', 'memory', 'trace', 'all'],
		type=str,
		metavar='{capture|memory|trace|all}',
		required=True)
	parser.add_argument('-profileunit', 
		type=str,
		metavar='${unitfile}',
		required=True)

	if '-type=capture' in sys.argv or '-type=all' in sys.argv:
		parser.add_argument('-capturetype',
			choices=['video', 'seq'],
			type=str,
			default='vedio',
			metavar="{video|seq}",
			required=False)
		parser.add_argument('-targetbuffers',
			type=str,
			metavar="${buffer1|buffer2|...|bufferN}",
			required=False)

	if '-type=memory' in sys.argv or '-type=all' in sys.argv:
		parser.add_argument('-dumpinterval',
			type=int,
			default=0,
			metavar="${interval}",
			required=False)

	if '-type=trace' in sys.argv or '-type=all' in sys.argv:
		parser.add_argument('-profiler', 
			type=str,
			choices=['csv', 'stat'],
			default='csv',
			metavar="{csv|stat}",
			required=False)

	parser.add_argument('-prefix', 
		type=str,
		metavar='${prefix}',
		required=False
		)

	now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
	parser.add_argument('-postfix', 
		type=str,
		metavar='${postfix}',
		default=now,
		required=False
		)

	profiledir = str()
	if ue4path.is_cwd_project_directory():
		profiledir = ue4path.get_project_directories()['profile_dir']
	if ue4path.is_cwd_packaging_directory():
		profiledir = ue4path.get_packaging_directories()['profile_dir']


	parser.add_argument('-profiledir', 
		type=str,
		default=profiledir,
		metavar='${profiledir}',
		required=False
		)

	ue4common.add_gameplay_options_argument(parser)	
	ue4common.add_log_options_argument(parser)

	# -------------------------------------- set func
	if '-type=capture' in sys.argv:
		parser.set_defaults(func=capturefunc);
	if '-type=memory' in sys.argv:
		parser.set_defaults(func=memoryfunc);
	if '-type=trace' in sys.argv:
		parser.set_defaults(func=tracefunc);
	if '-type=all' in sys.argv:
		parser.set_defaults(func=allfunc);

