import os
import sys


fspath = os.fspath if sys.version_info < (3, 11) else lambda x: x
