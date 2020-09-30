from pathlib import Path
import os.path
import sys

# EXPTN = "MB020_cb_R_g0"

root = Path("../")
if 'FILEPATH' not in locals():
    # FILEPATH = Path(os.path.join("/Volumes/bunaken/Marie", "npx", EXPTN))
    script_dir = os.path.dirname(__file__)
    rel_path = 'tests/testfiles'
    FILEPATH = Path(os.path.join(script_dir, rel_path))

figpathstr = "figs"

# if FILEPATH.exists():
#     module_path = '/params'
#     module_path = Path(os.path.join(FILEPATH, 'params'))
#     sys.path.append(module_path)

module_path = os.path.join(FILEPATH, 'params.py')
if module_path not in sys.path:
    sys.path.append(module_path)

full_path = os.path.join(FILEPATH)
if full_path not in sys.path:
    sys.path.append(full_path)

figpath = os.path.join(figpathstr)
if figpath not in sys.path:
    sys.path.append(figpath)