import sys, runpy
sys.argv=['r80.py','search','0','0']
try: runpy.run_path('r80.py', run_name='x')
except SystemExit: pass
