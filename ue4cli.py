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

project['uproject']						= project['base_dir'] + '\\' + project['name'] + '.uproject'
project['generate_project_file_bat']	= project['base_dir'] + '\\' + 'GenerateProjectFiles.bat'

project['server_exe']					= project['binary_dir'] + '\\' + project['name'] + 'Server.exe'
project['client_exe']					= project['binary_dir'] + '\\' + project['name'] + '.exe'


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
		print('\t{0:<26} = {1}'.format(key, val))
	print('')

def echo_cmd(exe, proj, opt):
	print('\t%s %s' % (exe, proj))
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

# -------------------------------------------------------- "env" command delegate
def env(args, remainder):
	print('#----------------------------------------------------- %s' % project['name'])
	echo_env(wkspace)
	echo_env(project)
	echo_env(engine)
	return ''

# -------------------------------------------------------- "build" command delegate
def build(args, remainder):
	cmd = ''
	cmd += engine['build_bat'] + ' '
	if args.target.lower() == 'game':
		cmd += project['name'] + ' '
	elif args.target.lower() == 'client':
		cmd += project['name'] + 'Client' + ' '
	elif args.target.lower() == 'server':
		cmd += project['name'] + 'Server' + ' '
	else :
		cmd += project['name'] + 'Editor' + ' '
	cmd += args.platform + ' '
	cmd += args.configuration + ' '
	cmd += project['uproject'] + ' '

	opt = [
		'-waitMutex',
		'-NoHotReload',
		' '.join(remainder),
	]
	return '%s%s' % (cmd, ' '.join(opt))

# -------------------------------------------------------- "editor" command delegate
def editor(args, remainder):
	cmd = ''
	cmd += engine['unreal_editor_cmd_exe'] + ' '
	cmd += project['uproject'] + ' '
	opt = [
		'-log',
		'-fullcrashdumpalways',
		'-ddc=noshared',
		' '.join(remainder),
	]
	return '%s%s' % (cmd, ' '.join(opt))

# -------------------------------------------------------- "server" command delegate
def server(args, remainder):
	cmd = ''
	if args.binary:
		cmd += 'TODO' + ' '
	else:
		cmd += engine['unreal_editor_cmd_exe'] + ' ' + project['uproject'] + ' '
	cmd += args.map + ' '

	opt = [
		'-server',
		'-game',
		'-fullcrashdumpalways',
		'-noailogging',
		'-NOSTEAM',
		'-log',
		' '.join(remainder)
	]
	return '%s%s' % (cmd, ' '.join(opt))

# -------------------------------------------------------- "game" command delegate
def game(args, remainder):
	cmd = ''
	if args.binary:
		cmd += 'TODO' + ' '
	else:
		cmd += engine['unreal_editor_cmd_exe'] + ' ' + project['uproject'] + ' '

	if args.standalone:
		cmd += args.map + ' '
	else:
		cmd += args.ip + ' '

	opt = [
	'-game',
	'-windowed',
	'-resx=1920',
	'-resy=1080',
	'-fullcrashdumpalways',
	'-noailogging',
	'-NOSTEAM',
	'-log',
	' '.join(remainder)
	]
	return '%s%s' % (cmd, ' '.join(opt))

# -------------------------------------------------------- "cook" command delegate
def cook(args, remainder):
	return ''

# -------------------------------------------------------- "profile" command delegate
def profile(args, remainder):
	return ''

# -------------------------------------------------------- main
def main(argc, argv):
	print('echo : %s' % ' '.join(sys.argv))
	if not is_valid_pwd():
		print('Failed to get valid pwd, %s' % wkspace['pwd_dir'])
		exit(0)

	# create the top-level parser
	main_parser = argparse.ArgumentParser()
	sub_parsers = main_parser.add_subparsers()

	# create the parser for the "env" command
	env_parser = sub_parsers.add_parser('env')
	env_parser.set_defaults(func=env)

	# create the parser for the "build" command
	build_parser = sub_parsers.add_parser('build')
	build_parser.add_argument('-target', '--target', type=str, default='editor')
	build_parser.add_argument('-platform', '--platform', type=str, default='Win64')
	build_parser.add_argument('-configuration', '--configuration', type=str, default='Development')
	build_parser.set_defaults(func=build)

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
	game_parser.add_argument('-map', type=str, default='DefaultStartMap')
	game_parser.add_argument('-standalone', '--standalone', action='store_true')
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
		if args.func == env:
			args.func(args, remainder)
			return


		env(args, remainder)
		print('# ------------------------------ launch')
		cmd = args.func(args, remainder)
		
		print(cmd)
		os.system(cmd)
		
	else:
		main_parser.print_help()


if __name__ == "__main__":
	main('', '')
