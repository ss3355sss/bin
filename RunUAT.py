import sys

from ue.env import *

def main(argc, argv):
	exec = argv[0]
	arguments = ' '.join(map(str, argv[1:]))
	print(exec)
	print(arguments)
	echo_env()

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)

	#print("cwd = %s" % cwd)
	#print("script_path 	= %s" % script_path)
	#print("script_dir	= %s" % script_dir)
    
	#print(get_uproject(cwd))
	#get_engine_association("%s\Dev.uproject" % cwd)
