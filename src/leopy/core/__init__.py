"""
core package

flo behaviors

"""
import importlib

_modules = ['resting', ]

for m in _modules:
    importlib.import_module(".{0}".format(m), package='leopy.core')
