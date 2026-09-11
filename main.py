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
from hid_functions import set_mode, set_colour, apply_mode_settings
from hid_functions import (
    set_streaming_speed,
    set_steady_brightness,
    set_breathing_speed,
    set_breathing_colour,
    set_breathing_colours,
    set_trail_speed,
    set_neon_speed,
    set_colourful_steady_colour,
    set_colourful_steady_colours,
    set_flicker_colour,
    set_flicker_colours,
    set_star_twinkle_speed,
    set_wave_speed,
)
from hid_functions import set_button, BUTTON_OFFSETS, ACTIONS

__all__ = [
    'VENDOR_ID',
    'PRODUCT_ID',
    'initialize',
    'get_battery',
    'set_mode',
    'set_colour',
    'apply_mode_settings',
    'set_streaming_speed',
    'set_steady_brightness',
    'set_breathing_speed',
    'set_breathing_colour',
    'set_breathing_colours',
    'set_trail_speed',
    'set_neon_speed',
    'set_colourful_steady_colour',
    'set_colourful_steady_colours',
    'set_flicker_colour',
    'set_flicker_colours',
    'set_star_twinkle_speed',
    'set_wave_speed',
    'set_button',
    'BUTTON_OFFSETS',
    'ACTIONS',
]
