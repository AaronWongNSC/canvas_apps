"""
Prevents console window from closing on error
"""

import sys
import traceback

def hold_window_on_error(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)    
    input("\nAn error occurred. Press [Enter] to exit...")
    sys.exit(-1)

sys.excepthook = hold_window_on_error
