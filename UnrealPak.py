import sys

from script.echo import *
from script.env import *

def main(argc, argv):
	exec = argv[0]
	arguments = ' '.join(map(str, argv[1:]))
	echo_env()
	execute(env['unreal_pak'], arguments)

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
