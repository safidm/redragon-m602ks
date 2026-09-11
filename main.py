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
from hid import VENDOR_ID, PRODUCT_ID
from hid import initialize
from hid import get_battery
from hid import set_mode, set_colour
from hid import set_button, BUTTON_OFFSETS, ACTIONS

# Re-export internal functions that some code may depend on
from hid.device import _build_device, _initialize_device, _get_current_state

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
