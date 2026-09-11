"""
DEPRECATED: This module is kept for backwards compatibility.
New code should import from the hid package directly.

Example:
    # Old way (still works):
    from main import initialize, set_mode, VENDOR_ID
    # New way (preferred):
    from hid import initialize, set_mode, VENDOR_ID
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

# Re-export everything from hid package for backwards compatibility
from hid_functions import VENDOR_ID, PRODUCT_ID
from hid_functions import initialize
from hid_functions import get_battery
from hid_functions import set_mode, set_colour
from hid_functions import set_button, BUTTON_OFFSETS, ACTIONS

__all__ = [
    'VENDOR_ID',
    'PRODUCT_ID',
    'initialize',
    'get_battery',
    'set_mode',
    'set_colour',
    'set_button',
    'BUTTON_OFFSETS',
    'ACTIONS',
]
