import sys

from script.echo import *
from script.env import *

'''
// Cooking

	
// Packaging
BuildCookRun -project=E:\wkspace\PUBG\ps5latest\Tsl\TslGame.uproject 
	-noP4 
	-platform=Win64 
	-clientconfig=Development 
	-serverconfig=Development 
	[-build] 
	-cook -iterativecooking / -skipcook
	[-MapsToCook=Baltic+...] 
	-stage / -skipstage
	[-pak] 
	-compressed 
	-archive 
	-archivedirectory=E:\wkspace\PUBG\ps5latest\_Package 
	-optimizematerialshaders 
	-UTF8Output
	-2017 
	-skipeditorbuild
'''

def main(argc, argv):
	exec = argv[0]
	arguments = ' '.join(map(str, argv[1:]))
	echo_env()

	if not arguments:
		arguments = "-help"

	execute(env['uat'], arguments)

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
