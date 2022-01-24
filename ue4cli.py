#set ue4 project configuration
import os
import sys
import argparse
import itertools
import subprocess 
# ----------------------------------------------------------------- Configuration
customized_project = [
	'Cowboy',
]

abs_path = os.path.abspath(os.getcwd())
base_dir = os.path.abspath((os.getcwd() + '\\..\\..\\'))

wkspace = dict()
wkspace['pwd_dir'] 		= os.path.abspath(os.getcwd())
wkspace['base_dir']		= os.path.abspath((os.getcwd() + '\\..\\..\\'))
wkspace['data_dir']		= wkspace['base_dir'] + '\\Data'
wkspace['editor_dir']	= wkspace['base_dir'] + '\\Editor'
wkspace['program_dir']	= wkspace['base_dir'] + '\\Program'

project = dict()
project['name']			= os.path.basename(os.getcwd())
project['base_dir']		= wkspace['program_dir'] + '\\' + project['name']
project['binary_dir']	= project['base_dir'] + '\\Binaries\\Win64' 
project['script_dir']	= project['base_dir'] + '\\Script' 
project['shader_dir']	= project['base_dir'] + '\\Shaders' 
project['saved_dir']	= project['base_dir'] + '\\Saved' 

project['server_exe']	= project['binary_dir'] + '\\' + project['name'] + 'Server.exe'
project['client_exe']	= project['binary_dir'] + '\\' + project['name'] + '.exe'


engine = dict()
if not project['name'] in customized_project:  
	engine['base_dir'] = 'C:\\Program Files\\Epic Games\\UE_4.26\\Engine'
else:
	engine['base_dir'] = wkspace['base_dir'] + '\\Program\\UnrealEngine\\Engine'
engine['binary_dir'] 			= engine['base_dir'] + '\\Binaries\\Win64'
engine['dotnet_dir'] 			= engine['base_dir'] + '\\Binaries\\DotNet'
engine['batch_dir'] 			= engine['base_dir'] + '\\Build\\BatchFiles'
engine['script_dir'] 			= engine['base_dir'] + '\\Script'
engine['shader_dir'] 			= engine['base_dir'] + '\\Shaders'
engine['saved_dir']				= engine['base_dir'] + '\\Saved'

engine['build_bat']				= engine['batch_dir'] + '\\Build.bat'
engine['runuat_bat']			= engine['batch_dir'] + '\\RunUAT.bat'

engine['unreal_editor_exe']		= engine['binary_dir'] + '\\UE4Editor.exe'
engine['unreal_editor_cmd_exe'] = engine['binary_dir'] + '\\UE4Editor-Cmd.exe'
engine['unreal_frontend_exe']	= engine['binary_dir'] + '\\UnrealFrontend.exe'
engine['unreal_insights_exe']	= engine['binary_dir'] + '\\UnrealInsights.exe'

engine['automation_tool_exe'] 	= engine['dotnet_dir'] + '\\AutomationTool.exe'

engine['csvcollate_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\CSVCollate.exe' 		
engine['csvconvert_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\CsvConvert.exe'
engine['csvfilter_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\CSVFilter.exe'
engine['csvinfo_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\csvinfo.exe'
engine['csvsplit_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\CSVSplit.exe'
engine['csvtosvg_exe'		] 	= engine['dotnet_dir'] + '\\CsvTools\\CSVToSVG.exe'
engine['perfreport_tool_exe'] 	= engine['dotnet_dir'] + '\\CsvTools\\PerfreportTool.exe'

# ----------------------------------------------------------------- Configuration end
def echo_env(env):
	if env == globals()['wkspace']:
		print('# ------------------------------ wkspace configuration')
	if env == globals()['project']:
		print('# ------------------------------ project configuration')
	if env == globals()['engine']:
		print('# ------------------------------ engine configuration')

	for key, val in env.items():
		print('\t{0:<24} = {1}'.format(key, val))

def echo_cmd(exe, opt):
	print('\t%s' % exe)
	for o in opt:
		print('\t\t%s' % o) 


def is_binary(v):
	if v:
		return 'TODO::' + ' '
	return engine['unreal_editor_exe'] + ' '

def is_exists(p):
	if os.path.exists(p):
		return True
	return False

def is_valid_pwd():
	if is_exists(wkspace['base_dir']) and is_exists(project['base_dir']) and is_exists(engine['base_dir']):
		return True
	return False;


def editor(args, remainder):
	cmd = engine['unreal_editor_exe']
	opt = [
		'-fullcrashdumpalways',
		'-ddc=noshared',
		' '.join(remainder),
	]
	return cmd, opt


def server(args, remainder):
	exe = is_binary(args.binary)
	if not is_exists(exe):
		return

	opt = [
		'-server',
		'-game',
		'-log',
		'-fullcrashdumpalways',
		'-noailogging',
		' '.join(remainder)
	]
	return exe, opt


def game(args, remainder):
	exe = is_binary(args.binary)

	if not args.standalone:
		exe += args.ip + ' '

	opt = [
	'-windowed',
	'-resx=1280',
	'-rey=720',
	'-game',
	'-log',
	'-fullcrashdumpalways',
	'-noailogging',
	'-NOSTEAM',
	' '.join(remainder)
	]
	return exe, opt
	#echo_cmd(exe, opt)
	#return '%s %s' % (exe, ' '.join(opt))


def cook(args, remainder):
	# TODO::
	pass


def profile(args, remainder):
	# TODO::
	pass


if __name__ == "__main__":
	print('echo : %s' % ' '.join(sys.argv))
	if not is_valid_pwd():
		print('Failed to get valid pwd, %s' % wkspace['pwd_dir'])
		exit(0)

	# create the top-level parser
	main_parser = argparse.ArgumentParser()
	sub_parsers = main_parser.add_subparsers()

	# create the parser for the "editor" command
	editor_parser = sub_parsers.add_parser('editor')
	editor_parser.set_defaults(func=editor)


	# create the parser for the "server" command
	server_parser = sub_parsers.add_parser('server')
	server_parser.add_argument('-b', '--binary', action='store_true')
	server_parser.add_argument('-map', type=str, default='DefaultStartMap')
	server_parser.set_defaults(func=server)


	# create the parser for the "game" command
	game_parser = sub_parsers.add_parser('game')
	game_parser.add_argument('-b', '--binary', action='store_true')
	game_parser.add_argument('-s', '--standalone', action='store_true')
	game_parser.add_argument('-ip', '--ip', type=str, default='127.0.0.1')
	game_parser.set_defaults(func=game)

	# create the parser for the "cook" command
	cook_parser = sub_parsers.add_parser('cook')
	cook_parser.set_defaults(func=cook)

	# create the parser for the "profile" command
	profile_parser = sub_parsers.add_parser('profile')
	profile_parser.set_defaults(func=profile)

	args, remainder = main_parser.parse_known_args()
	if hasattr(args, "func"):
		echo_env(wkspace)
		echo_env(project)
		echo_env(engine)

		print('# ------------------------------ launch')
		exe, opt = args.func(args, remainder)

		print('\t%s' % exe)
		for o in opt:
			print('\t\t%s' % o) 

		command = '%s %s' % (exe, ' '.join(opt))
		print(command)

	else:
		main_parser.print_help()

