import sys
from pathlib import Path

# add ability to run tests using make file
src_path = Path('.', 'src').resolve()
sys.path.append(str(src_path))
