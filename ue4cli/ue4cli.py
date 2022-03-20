#!/usr/bin/env python

import os
import sys
if os.path.islink(__file__):
	# workaround for using symbolic link in windows
	sys.path.append(os.path.dirname(os.readlink(__file__)))
import argparse

from stdout import * 

from ue4sys import path as ue4path

from ue4cmd import common as ue4common
from ue4cmd import editor as ue4editor

from ue4cmd import build as ue4build
from ue4cmd import package as ue4package


from ue4cmd import game as ue4game
from ue4cmd import client as ue4client
from ue4cmd import server as ue4server
from ue4cmd import profile as ue4profile


def add_parser(cmd, sub_parser):
	parser = cmd.add_parser(sub_parser)
	if not parser:
		return False
	ue4common.add_global_argument(parser)	
	cmd.add_argument(parser)

	return True

def main(argc, argv):
	if not ue4path.get_project():
		warning('Failed to get valid -project=\'${project}\' in %s' % (os.getcwd()))
		return None

	main_parser = argparse.ArgumentParser()
	sub_parser = main_parser.add_subparsers()

	if ue4path.is_cwd_project_directory():
		add_parser(ue4editor, sub_parser)
		add_parser(ue4build, sub_parser)
		add_parser(ue4package, sub_parser)
	
	if ue4path.is_cwd_project_directory() or ue4path.is_cwd_packaging_directory():
		add_parser(ue4game, sub_parser)
		add_parser(ue4client, sub_parser)
		add_parser(ue4server, sub_parser)
		add_parser(ue4profile, sub_parser)
	else:
		warning('Failed to get valid -project=\'${project}\' in %s' % (os.getcwd()))
		return


	args, remainder = main_parser.parse_known_args()

	if hasattr(args, "func"):
		args.func(args, remainder)
	else:
		main_parser.print_help()

if __name__ == "__main__" and __package__ is None:
	main(len(sys.argv), sys.argv)
