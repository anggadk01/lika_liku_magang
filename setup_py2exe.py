from distutils.core import setup
import py2exe
import glob
import os
import sys
import itertools

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin"))

options = {"py2exe": {"compressed": 0,
						"optimize": 2,
						"packages": ["encodings","mx.DateTime","wizard","pychart","PIL", "pyparsing", "pydot"],
						"excludes" : ["Tkconstants","Tkinter","tcl"],
						}}

data_files = []

os.chdir('bin')
for (dp,dn,names) in os.walk('addons'):
	if '.svn' in dn:
		dn.remove('.svn')
	data_files.append((dp, map(lambda x: os.path.join('bin', dp,x), names)))
for (dp,dn,names) in os.walk('i18n'):
	if '.svn' in dn:
		dn.remove('.svn')
	data_files.append((dp, map(lambda x: os.path.join('bin', dp,x), names)))
os.chdir('..')
for (dp,dn,names) in os.walk('doc'):
	if '.svn' in dn:
		dn.remove('.svn')
	data_files.append((dp, map(lambda x: os.path.join(dp,x), names)))

setup(
	name="tinyerp-server",
	console = [{"script":"bin\\tinyerp-server.py", "icon_resources":[(1,"pixmaps\\tinyerp.ico")]}],
	data_files = data_files,
	options = options
	)