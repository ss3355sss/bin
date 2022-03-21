# #!/usr/bin/env python
import os
import sys

import argparse
import datetime
from distutils.util import strtobool

import subprocess 
from subprocess import Popen, PIPE
from stdout import * 

from ue4sys import path as ue4path

def get_command(execute, arguments, remainder = None):
	project = ue4path.get_project()
	if project:
	 	display('project')
	 	print('   ', end='')
	 	print('%s' % project)
	 	print()

	if execute:
		display("execute")
		print('   ', end='')
		for string in execute.split(' '):
			print('%s' % os.path.basename(string), end=' ')
		print('\n')

	if arguments:
		display("arguments")
		for arg in arguments:
			print('   %s' % arg)
		if remainder:
			print('   %s' % remainder)
			arguments.append(remainder)
		print()

	command = '%s %s' % (execute, (' ').join(arguments))

	display("command")
	print('   %s' % command)
	print()

	#Todo:: 뭐가 더 좋은거임
	#with Popen([command, arguments], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
	#	for line in p.stdout:
	#		print(line, end='') 
	os.system(command)


	return command

def get_remainder(remainder):
	remainder = [remain for remain in remainder if not remain.startswith('-project')]
	return remainder


def add_global_argument(parser):
	pass

def add_global_options():
	pass

def add_gameplay_execute_argument(parser):
	if ue4path.is_cwd_project_directory():
		parser.add_argument('-uncooked', action='store_true')


def get_gameplay_execute(args, is_server):
	execute = str()

	if ue4path.is_cwd_project_directory():
		if not ue4path.is_engine_directory_valid():
			error('Failed to get valid engine directory')
			return str()

		engine_dirs 	= ue4path.get_engine_directories()
		project_dirs 	= ue4path.get_project_directories()
		
		if args.uncooked:
			if is_server:
				execute = '%s' % project_dirs['server']
			else:
				execute = '%s' % project_dirs['client']
		else:
			execute = '%s %s' % (engine_dirs['ue4editor'], project_dirs['uproject'])

	if ue4path.is_cwd_packaging_directory():

		execute = '%s' % ue4path.get_packaging_directories()['client']

	return execute


def add_gameplay_options_argument(parser):
	parser.add_argument('-windowed', type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-resx', type=int, default=1024, metavar="${resx}", required=False)
	parser.add_argument('-resy', type=int, default=768, metavar="${resx}", required=False)

	parser.add_argument('-noailogging',  		type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-noverifygc', 			type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-nosteam', 			type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-fullcrashdumpalways', type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)

def get_gameplay_options(args, is_server):
	opts = list()
	if args.windowed:
		opts.append('-windowed')
		opts.append('-resx=%s' % args.resx)
		opts.append('-resy=%s' % args.resy)

	if args.noailogging:
		opts.append('-noailogging')

	if args.noverifygc:
		opts.append('-noverifygc')

	if args.nosteam:
		opts.append('-nosteam')

	if args.fullcrashdumpalways:
		opts.append('-fullcrashdumpalways')

	if is_server:
		opts.append('-server')

	opts.append('-game')


	return opts



def add_log_options_argument(parser):
	parser.add_argument('-log', action='store_true')
	parser.add_argument('-logcmds', type=str, metavar="${categories}", required=False)

def get_log_options(args):
	opts = list()
	if args.log:
		opts.append('-log')
		if args.logcmds:
			categories = '\"global off, %s\"' % args.logcmds
			opts.append('-logcmds=%s' % categories)
	else:
		opts.append('-silent')
	return opts

