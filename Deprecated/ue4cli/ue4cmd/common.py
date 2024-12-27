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

def exec_command(execute, params, options, remainder = None):
	project = ue4path.get_project()
	if project:
	 	display('project')
	 	print('   ', end='')
	 	print('%s' % project)
	 	print()

	if params:
		display("params")
		for param in params:
			print('   %s' % param)
		print('')

	if options:
		display("options")
		for opt in options:
			print('   %s' % opt)
		if remainder:
			print('   %s' % remainder)
			options.append(remainder)
		print()

	command = execute
	arguments = '%s %s' % (' '.join(params), ' '.join(options))

	display("command")
	print('   %s %s' % (execute, arguments))
	print()

	#os.system('%s %s' % (execute, arguments))
	proc = subprocess.Popen('%s %s' % (execute, arguments))
	out, err = proc.communicate()

def get_remainder(remainder):
	remainder = [remain for remain in remainder if not remain.startswith('-project')]
	return remainder


def add_global_argument(parser):
	pass

def add_global_options():
	pass

def add_gameplay_execute_argument(parser):
	if ue4path.is_cwd_project_directory():
		parser.add_argument('-cooked', action='store_true')

		#project = ue4path.get_project()
		#stage_dir = ue4path.get_project_directories()['stage_dir']
		parser.add_argument('-stagedir', 
			type=str,
			default=ue4path.get_project_directories()['stage_dir'],
			metavar='${statedir}\\${Target}\\%s\\Binaries\\Win64' % ue4path.get_project(), 
			required=False)

def get_gameplay_execute(args, is_server):
	execute = str()
	params = list()
	options = list()

	if ue4path.is_cwd_project_directory():
		if not ue4path.is_engine_directory_valid():
			error('Failed to get valid engine directory')
			return str()

		engine_dirs 	= ue4path.get_engine_directories()
		project_dirs 	= ue4path.get_project_directories()
		
		if args.cooked:
			stage_dir = str()
			project = ue4path.get_project()
			stage_dir = ue4path.get_project_directories()['stage_dir']

			if is_server:
				execute = '%s' % project_dirs['server']
				options.append('-basedir=%s\\WindowsServer\\%s\\Binaries\\Win64' % (args.stagedir, ue4path.get_project()))
			else:
				print(args.stagedir)
				execute = '%s' % project_dirs['client']
				options.append('-basedir=%s\\WindowsNoEditor\\%s\\Binaries\\Win64' % (args.stagedir, ue4path.get_project()))
		else:
			execute = '%s' % engine_dirs['ue4editor']
			params.append('%s' % project_dirs['uproject'])

	elif ue4path.is_cwd_packaging_directory():
		if is_server:
			execute = '%s' % ue4path.get_packaging_directories()['server']
		else:
			execute = '%s' % ue4path.get_packaging_directories()['client']		

	return execute, params, options


def add_additional_gameplay_options_argument(parser):
	parser.add_argument('-noailogging',  		type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-noverifygc', 			type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-nosteam', 			type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-fullcrashdumpalways', type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)

def get_additional_gameplay_options(args, is_server):
	opts = list()
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

def add_gamewnd_options_argument(parser):
	parser.add_argument('-windowed', type=lambda x:bool(strtobool(x)), default=True, metavar="{true|false}", required = False)
	parser.add_argument('-resx', type=int, default=1024, metavar="${resx}", required=False)
	parser.add_argument('-resy', type=int, default=768, metavar="${resx}", required=False)

def get_gamewnd_options(args):
	opts = list()
	if args.windowed:
		opts.append('-windowed')
		opts.append('-resx=%s' % args.resx)
		opts.append('-resy=%s' % args.resy)	
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

