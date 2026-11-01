import sys, runpy
sys.argv = ['r56.py', 'search', '0', '0']
try: g = runpy.run_path('r56.py')
except SystemExit: pass
