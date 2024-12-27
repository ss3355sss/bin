import subprocess
import sys

from script.env import *

def main(argc, argv):
	process = subprocess.Popen('%s' % env['unreal_insights'])
	if process.stderr:
		fatal(process.stderr.readlines())
	out, err = process.communicate()
	


if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
