import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('wyrmy.py', base=base, targetName='Wyrmy.exe')
]

setup(name='Wyrmy',
      version='1.0',
      author='Avirut Mehta',
      description='C. elegans scoring aid',
      options=options,
      executables=executables
      )