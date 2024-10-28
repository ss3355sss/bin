import os
import glob
import json
import winreg


from ue.echo import *


_name_ = dict()
_required_ = dict()
_optional_ = dict()
env = dict()

def get_uproject(directory):
    uprojects = glob.glob(os.path.join(directory, '*.uproject'))
    if len(uprojects) == 0:
        error("Failed to get valid uproject: %s" % directory)
        exit()
    return uprojects[0]

def get_engine_association(uproject_path):
    if not os.path.exists(uproject_path):
        error("Failed to get valid uproject_path: %s" % uproject_path)
        exit()

    with open(uproject_path, 'r') as file:
        uproject_data = json.load(file)
    engine_association = uproject_data.get('EngineAssociation', 'Failed to get EngineAssociation Field.')
    return engine_association 

def get_engine_directory(engine_association):
    key_path = r"SOFTWARE\Epic Games\Unreal Engine\Builds"

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(registry_key, engine_association)
        winreg.CloseKey(registry_key)
    except FileNotFoundError:
        error(f"Registry path does not exist: {key_path, engine_association}")
        exit()
    
    except PermissionError:
        error(f"Permission to access the registry is denied: {key_path, engine_association}")
        exit()
    return value

def get_engine_version(version_path):
    try:
        with open(version_path, 'r') as file:
            # JSON 데이터 파싱
            data = json.load(file)
            
            # MajorVersion, MinorVersion, PatchVersion 추출
            major_version = data.get("MajorVersion")
            minor_version = data.get("MinorVersion")
            patch_version = data.get("PatchVersion")
            
            return major_version, minor_version, patch_version
    
    except FileNotFoundError:
        error(f"Failed to get valid version_path: {version_path}")
        exit()
    
    except json.JSONDecodeError:
        print(f"JSON syntax error occurred in the file.: {version_path}")
        exit()

def validate(dictionary, is_requried):
    for key, val in dictionary.items():
        if not os.path.exists(val):
            print({key, val})
            raise FileNotFoundError(f"File or directory does not exist: {key, val}")

def echo_env():
	for key, val in env.items():
		display('\t{0:<26} = {1}'.format(key, val))
	print('')

try:
    _required_['cwd']          = os.getcwd()
    _required_['script_path']  = os.path.abspath(__file__)      
    _required_['script_dir']   = os.path.dirname(_required_['script_path'])

    _required_['uproject'] = get_uproject(_required_['cwd'])
    _name_['project']  = os.path.splitext(os.path.basename(_required_['uproject']))[0]
    _name_['engine_association'] = get_engine_association(_required_['uproject'])

    _required_['engine_dir'] = get_engine_directory(_name_['engine_association'])
    _name_['engine_major_version'], _name_['engine_minor_version'], _name_['engine_patch_version'] = get_engine_version("%s\\Engine\\Build\\Build.version" % _required_['engine_dir'])

    _required_['ubt'] = '%s\\Engine\\Binaries\\DotNet\\UnrealBuildTool\\UnrealBuildTool.dll' % _required_['engine_dir']
    _required_['uat'] = '%s\\Engine\\Binaries\\DotNet\\AutomationTool\\AutomationTool.exe' % _required_['engine_dir']

    if _name_['engine_major_version'] >= 5:
        _optional_['unreal_insights'] = '%s\\Engine\\Binaries\\Win64\\UnrealInsights.exe'

    if _name_['engine_minor_version'] >= 27:
        _optional_['csvcollect'] = '%s\\Engine\\Binaries\\DotNet\\CSVCollate.exe'
        _optional_['csvconvert'] = '%s\\Engine\\Binaries\\DotNet\\CsvConvert.exe'
        _optional_['csvfilter'] = '%s\\Engine\\Binaries\\DotNet\\CSVFilter.exe'
        _optional_['csvinfo'] = '%s\\Engine\\Binaries\\DotNet\\csvinfo.exe'
        _optional_['csvsplit'] = '%s\\Engine\\Binaries\\DotNet\\CSVSplit.exe'
        _optional_['csvtosvg'] = '%s\\Engine\\Binaries\\DotNet\\CSVToSVG.exe'
        _optional_['perfreport_tool'] = '%s\\Engine\\Binaries\\DotNet\\PerfreportTool.exe'

    validate(_required_, True)
    env = {**_name_, **_required_, **_optional_}

except FileNotFoundError as e:
    error(e)
    exit()
          
except Exception as e:
    error("Failed to set valid environment ue configuration: %s" % e)
    exit()

