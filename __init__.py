from pathlib import Path
import os.path
import sys

EXPTN = "MB020_cb_R_g0"

root = Path("../")
FILEPATH = Path(os.path.join("/Volumes/bunaken/Marie", "npx", EXPTN))

figpath = "figs"

# if FILEPATH.exists():
#     module_path = '/params'
#     module_path = Path(os.path.join(FILEPATH, 'params'))
#     sys.path.append(module_path)

module_path = os.path.join(FILEPATH, 'params.py')
if module_path not in sys.path:
    # sys.path.append('/path/to/application/app/folder')
    sys.path.append(module_path)

full_path = os.path.join(FILEPATH)
if full_path not in sys.path:
    sys.path.append(full_path)

figpath = os.path.join(figpath)
if figpath not in sys.path:
    sys.path.append(figpath)

# Load whisking data
# if '../../' not in sys.path:
#     sys.path.append('../../')
