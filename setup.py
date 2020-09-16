from setuptools import setup
import os


def _package_tree(pkgroot):
    path = os.path.dirname(__file__)
    subdirs = [os.path.relpath(i[0], path).replace(os.path.sep, '.')
               for i in os.walk(os.path.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


curdir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(curdir, 'README.md')) as f:
    readme = f.read()


with open('requirements.txt') as f:
    require = [x.strip() for x in f.readlines() if not x.startswith('git+')]

setup(
   name='cb_recordings',
   version='1.0',
   license="BSD",
   long_description=readme,
   description='A useful module',
   author='Marie Tolkiehn',
   author_email='marie_tol@hotmail.com',
   packages=_package_tree('cb_recordings'),
   install_requires=require,  # external packages as dependencies
   include_package_data=True
)

#
# from pathlib import Path
# import os.path
# import sys
#
# EXPTN = "MB020_cb_R_g0"
#
# root = Path("../")
# FILEPATH = Path(os.path.join("/Volumes/bunaken/Marie", "npx", EXPTN))
#
# figpath = "figs"
# # figpath = root / ".." / "npx" / "figs"
#
# # if FILEPATH.exists():
#     # module_path = '/params'
# module_path = os.path.join(FILEPATH, 'params.py')
# if module_path not in sys.path:
#     sys.path.append(module_path)
#
# full_path = os.path.join(FILEPATH)
# if full_path not in sys.path:
#     sys.path.append(full_path)
#
# figpath = os.path.join(figpath)
# if figpath not in sys.path:
#     sys.path.append(figpath)
#
# # Load whisking data
# if '../../' not in sys.path:
#     sys.path.append('../../')
