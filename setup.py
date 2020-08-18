from pathlib import Path
import os.path
import sys

exptn = "MB020_cb_R_g0"

root = Path("../")
filepath = Path(os.path.join("/Volumes/Marie", "npx", exptn))

figpath = "figs"
# figpath = root / ".." / "npx" / "figs"

if filepath.exists():
    module_path = '/params'

full_path = os.path.join(filepath)
if full_path not in sys.path:
    sys.path.append(full_path)

figpath = os.path.join(figpath)
if figpath not in sys.path:
    sys.path.append(figpath)

# Load whisking data
if '../../' not in sys.path:
    sys.path.append('../../')