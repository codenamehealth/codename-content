import sys, os, runpy
# run r80 sim only: execute the file up to the 'search' branch by faking argv
sys.argv = ['r80.py', 'search', '0', '0']
try: runpy.run_path('r80.py', run_name='__main__')
except SystemExit: pass
