#!/usr/bin/env python

import os
import sys
import re

def echo_directories(directories):
	for name, directory in dirs.items():
		print('   {0:<26} = {1}'.format(name, directory))

def get_project():
	project = str()

	match = re.search(r'-project=[a-zA-Z0-9]+', ' '.join(sys.argv))
	if match:
		project = match.group().split('=')[1]

	match = re.search(r'-project [a-zA-Z0-9]+', ' '.join(sys.argv))
	if match:
		project = match.group().split(' ')[1]
	if not project:
		return False
	return project

def is_exist(path):
	if os.path.exists(path):
		basename = os.path.basename(path)
		parent_dir = os.path.dirname(path)
		if basename in os.listdir(parent_dir):
			return True
		return False
	return False

def is_required_directory_valid(directories):
	if not directories:
		return False

	for key, value in directories.items():
		if not is_exist(value):
			return False
	return True

def get_project_directories(workingdirectory = os.getcwd()) -> dict :
	project = get_project()
	if not project:
		return dict()

	dirs = dict()

	# -------------------------------------- Required Paths
	dirs['uproject']		= '%s\\%s.uproject' 	% (workingdirectory, project)

	if not is_required_directory_valid(dirs):
		return dict()

	# -------------------------------------- Optional Paths
	dirs['binary_dir'] 		= '%s\\Binaries\\Win64' % workingdirectory
	dirs['script_dir'] 		= '%s\\Script' 			% workingdirectory
	dirs['shader_dir'] 		= '%s\\Shaders' 		% workingdirectory
	dirs['saved_dir']		= '%s\\Saved' 			% workingdirectory

	dirs['profile_dir']		= '%s\\Profile' 		% dirs['saved_dir']
	dirs['stage_dir']		= '%s\\StagedBuilds' 	% dirs['saved_dir']
	dirs['archive_dir']		= '%s\\Archive' 		% dirs['saved_dir']

	dirs['client']			= '%s\\%s.exe' 		 	% (dirs['binary_dir'], project)
	dirs['server']			= '%s\\%sServer.exe' 	% (dirs['binary_dir'], project)

	return dirs;

def get_packaging_directories(workingdirectory = os.getcwd()):
	project = get_project()
	if not project:
		return dict()

	apptype = None
	if is_exist('%s\\%s.exe' % (workingdirectory, project)):
		apptype = 'client'
	elif is_exist('%s\\%sServer.exe' % (workingdirectory, project)):
		apptype = 'server'
	else:
		return dict()


	dirs = dict()
	# -------------------------------------- Required Paths
	game_dir 			= '%s\\%s' 				% (workingdirectory, project)
	dirs['binary_dir'] 	= '%s\\Binaries\\Win64' % game_dir

	engine_dir 					= '%s\\Engine' 			% workingdirectory
	#dirs['engine_binary_dir'] 	= '%s\\Binaries\\Win64' % engine_dir

	if not is_required_directory_valid(dirs):
		return dict()

	# -------------------------------------- Optional Paths
	dirs['script_dir'] 	= '%s\\Script' 			% game_dir
	dirs['shader_dir'] 	= '%s\\Shaders' 		% game_dir
	dirs['saved_dir'] 	= '%s\\Saved' 			% game_dir
	dirs['profile_dir'] = '%s\\Saved\\Profile' 	% game_dir
	if apptype == 'client':
		dirs['client'] 			= '%s\\%s.exe' % (dirs['binary_dir'], project)
	if apptype == 'server':
		dirs['server'] 			= '%s\\%sServer.exe' % (dirs['binary_dir'], project)

	return dirs

def get_engine_directories(workingdirectory = os.getcwd()):
	candidates = [
		'%s\\UnrealEngine\\Engine' % workingdirectory,
		'%s\\UnrealEngine\\Engine' % os.path.dirname(workingdirectory),
		'%s\\Engine' % workingdirectory
	]
	engine_dir = next((candidate for candidate in candidates if is_exist(candidate)), None)
	if not engine_dir:
		return dict()

	dirs = dict()
	# -------------------------------------- Required Paths
	dirs['binary_dir'] 			= '%s\\Binaries\\Win64' 	% engine_dir
	dirs['dotnet_dir'] 			= '%s\\Binaries\\DotNET' 	% engine_dir
	dirs['batch_dir'] 			= '%s\\Build\\BatchFiles' 	% engine_dir
	dirs['shader_dir'] 			= '%s\\Shaders' 			% engine_dir
	dirs['saved_dir']			= '%s\\Saved' 				% engine_dir

	dirs['build']				= '%s\\Build.bat' 			% dirs['batch_dir']
	dirs['runuat']				= '%s\\RunUAT.bat' 			% dirs['batch_dir']

	#dirs['ue4editor']		= '%s\\UE4Editor.exe' 		% dirs['binary_dir']
	dirs['ue4editor'] 	= '%s\\UE4Editor-Cmd.exe' 	% dirs['binary_dir']

	if not is_required_directory_valid(dirs):
		return dict()


	# -------------------------------------- Optional Paths
	dirs['script_dir'] 			= '%s\\Script' 				% engine_dir

	dirs['unreal_frontend']		= '%s\\UnrealFrontend.exe' 	% dirs['binary_dir']
	dirs['unreal_insights']		= '%s\\UnrealInsights.exe' 	% dirs['binary_dir']

	dirs['automation_tool'] 	= '%sAutomationTool.exe' 			% dirs['dotnet_dir']
	dirs['csvcollate'] 			= '%sCsvTools\\CSVCollate.exe' 		% dirs['dotnet_dir']
	dirs['csvconvert'] 			= '%sCsvTools\\CsvConvert.exe' 		% dirs['dotnet_dir']
	dirs['csvfilter'] 			= '%sCsvTools\\CSVFilter.exe' 		% dirs['dotnet_dir']
	dirs['csvinfo'] 			= '%sCsvTools\\csvinfo.exe' 		% dirs['dotnet_dir']
	dirs['csvsplit'] 			= '%sCsvTools\\CSVSplit.exe' 		% dirs['dotnet_dir']
	dirs['csvtosvg'] 			= '%sCsvTools\\CSVToSVG.exe' 		% dirs['dotnet_dir']
	dirs['perfreport_tool'] 	= '%sCsvTools\\PerfreportTool.exe' 	% dirs['dotnet_dir']

	return dirs;

def is_cwd_project_directory(workingdirectory = os.getcwd()):
	if not get_project_directories(workingdirectory):
		return False
	return True

def is_cwd_packaging_directory(workingdirectory = os.getcwd()):
	if not get_packaging_directories(workingdirectory):
		return False
	return True


def is_engine_directory_valid(workingdirectory = os.getcwd()):
	if not get_engine_directories(workingdirectory):
		return False
	return True



