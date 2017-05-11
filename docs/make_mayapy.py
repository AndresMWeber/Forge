#!C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe
print "Running mayapy from make_mayapy.py"
import maya.standalone
maya.standalone.initialize(name='python')
import sphinx
import sys
import os

if __name__ == '__main__':
    argv = sys.argv[1:]
    cwd = os.getcwd()
    argv.insert(0, sphinx.__file__)
    sphinx.main(argv)
