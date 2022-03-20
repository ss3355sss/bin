#set ue4 project configuration
import os
import sys

import datetime

import argparse
import itertools
import subprocess 
from subprocess import Popen, PIPE


def profilingdirfunc(args, remainder):
	cmd = ''

	if args.profilingdir:
		cmd += ' profilingdir=%s' % args.profilingdir
	if args.prefix:
		cmd += ' prefix=%s' % args.prefix
	if args.postfix:
		cmd += ' postfix=%s' % args.postfix


	return cmd

def capturefunc(args, remainder):
	# Cowboy.exe -bv.profile phase=capture, capturetype={video|sequence}[, ...]
	cmd = '-phase=capture '
	cmd += '-capturetype=%s ' % args.capturetype
	if args.targetbuffers:
		cmd += '-targetbuffers=%s' % args.targetbuffers

	cmd += profilingdirfunc(args, remainder)

	return cmd

def memoryusagefunc(args, remainder):
	# Cowboy.exe -bv.profile phase=memoryusage, [dumpinterval=${int}][, ...]
	cmd = '-phase=memoryusage '
	cmd += '-dumpinterval=%d ' % args.dumpinterval

	cmd += profilingdirfunc(args, remainder)

	return cmd

def tracefunc(args, remainder):
	# Cowboy.exe -bv.profile phase=trace, -profiler={csv|stat}[, ...]
	cmd = '-phase=trace '
	cmd += '-profiler=%s ' % args.profiler

	cmd += profilingdirfunc(args, remainder)

	return cmd

def allfunc(args, remainder):
	cmd = list()
	cmd.append(capturefunc(args, remainder))
	cmd.append(memoryusagefunc(args, remainder))
	cmd.append(tracefunc(args, remainder))

	return cmd

def add_profilingdir_argument(parser):
	# bvprofile.py 
	#	...
	#	[-profilingdir=${dir}]
	#	[-prefix=${prefix}]
	#	[-postfix=${postfix}]	
	parser.add_argument('-profilingdir', 
		help='path to profile folder',
		type=str,
		required=False)
	parser.add_argument('-prefix', 
		help='path to add profile folder prefix',
		type=str,
		required=False)
	parser.add_argument('-postfix', 
		help='path to add profile folder postfix',
		type=str,
		required=False)


def add_capture_argument(parser):
	# bvprofile.py capture
	#	-capturetype={video|sequnece}
	#	[-targetbuffers=${buffer0|buffer1|...|bufferN}]
	#	...
	parser.add_argument('-capturetype', 
		type=str,
		choices=['video', 'sequnce'],
		default='video',
		required=True)
	parser.add_argument('-targetbuffers',
		type=str,
		required=False)	

def add_memoryusage_argument(parser):
	# bvprofile.py memoryusage
	#	[-dumpinterval=${int}]
	#	...
	parser.add_argument('-dumpinterval', 
		type=int,
		default='0',
		required=False)

def add_trace_argument(parser):
	# bvprofile.py 
	#	-profiler={csv|stat}
	#	...
	parser.add_argument('-profiler', 
		type=str,
		choices=['csv', 'stat'],
		default='csv',
		required=True)


# -------------------------------------------------------- main
def main(argc, argv):
	sec = 0
	if argc == 1:
		sec = 4
	else:
		sec = argv[1];

	main_parser = argparse.ArgumentParser()
	main_parser.add_argument('-profilingdir', '--profilingdir', 
		help='path to profile folder',
		type=str,
		required=False)
	main_parser.add_argument('-prefix', '--prefix', 
		help='path to add profile folder prefix',
		type=str,
		required=False)
	main_parser.add_argument('-postfix', '--postfix', 
		help='path to add profile folder postfix',
		type=str,
		required=False)

	sub_parsers = main_parser.add_subparsers()

	# Create "Capture" Argument Parser
	capture_parser = sub_parsers.add_parser('capture', help='capture phase')
	add_capture_argument(capture_parser)
	add_profilingdir_argument(capture_parser)
	capture_parser.set_defaults(func=capturefunc);

	# Create "MemoryUsage" Argument Parser
	memoryusage_parser = sub_parsers.add_parser('memoryusage', help='memoryusage phase')
	add_memoryusage_argument(memoryusage_parser)
	add_profilingdir_argument(memoryusage_parser)
	memoryusage_parser.set_defaults(func=memoryusagefunc);

	# Create "Trace" Argument Parser
	trace_parser = sub_parsers.add_parser('trace', help='trace phase')
	add_trace_argument(trace_parser)
	add_profilingdir_argument(trace_parser)
	trace_parser.set_defaults(func=tracefunc);

	# Create "All" Argument Parser
	all_parser = sub_parsers.add_parser('all', help='all profile phase(capture > memoryusage > trace)')
	add_capture_argument(all_parser)
	add_memoryusage_argument(all_parser)
	add_trace_argument(all_parser)
	add_profilingdir_argument(all_parser)
	all_parser.set_defaults(func=allfunc);

	#args, remainder = main_parser.parse_args()
	args, remainder = main_parser.parse_known_args()

	now = datetime.datetime.now()
	nowTime = now.strftime('%Y_%m_%d-%H_%M_%S')
	print(nowTime)  # 2015-04-19 12:11:32


	if hasattr(args, "func"):
		if args.func == capturefunc:
			cmd = args.func(args, remainder)
			print('bv.profile %s' % cmd)

		if args.func == memoryusagefunc:
			cmd = args.func(args, remainder)
			print('bv.profile %s' % cmd)

		if args.func == tracefunc:
			cmd = args.func(args, remainder)
			print('bv.profile %s' % cmd)

		if args.func == allfunc:
			cmds = args.func(args, remainder)
			for cmd in cmds:
				print('bv.profile %s' % cmd)
	else:
		main_parser.print_help()
	
	# create the parser for the "build" command
	#build_parser = sub_parsers.add_parser('')
	#build_parser.add_argument('-target', '--target', type=str, default='editor')
	#build_parser.add_argument('-platform', '--platform', type=str, default='Win64')
	#build_parser.add_argument('-configuration', '--configuration', type=str, default='Development')
	#build_parser.set_defaults(func=build)


	#command = 'sleep.exe'
	#with Popen([command, sec], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
	#	for line in p.stdout:
	#		print(line, end='') 

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
