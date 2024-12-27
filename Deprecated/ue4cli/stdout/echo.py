#!/usr/bin/env python

DEBUG = True

HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def debug(string):
	if DEBUG:
		print('%s' % string)

def log(string):
	print('%s' % string)

def display(string):
	print(CYAN + string + ENDC)

def error(string):
	print(FAIL + string + ENDC)

def warning(string):
	print(WARNING + string + ENDC)

# def echo_command(execute=None, params=None, opts=None):
# 	if execute:
# 		display("execute")
# 		print('   %s' % os.path.basename(execute))
# 		print()
		
# 	if params:
# 		display("params")
# 		for param in params.split(' '):
# 			print("   %s" % os.path.basename(param))
# 	if opts:
# 		display("opts")
# 		for opt in opts.split(' '):
# 			print("   %s" % opt)