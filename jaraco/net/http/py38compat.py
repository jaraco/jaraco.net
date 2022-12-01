import os
import sys


fspath = os.fspath if sys.version_info < (3, 9) else lambda x: x
