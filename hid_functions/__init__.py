"""
HID communication layer for Redragon M602KS mouse.

This module provides low-level hardware interface functions for:
- Device initialization and access
- Battery monitoring
- RGB lighting control (modes and colors)
- Button remapping

All functions communicate with the mouse via USB HID protocol.
"""

from .constants import VENDOR_ID, PRODUCT_ID
from .device import initialize
from .battery import get_battery
from .lighting import (
    set_mode,
    set_colour,
    apply_mode_settings,
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
from .buttons import set_button, BUTTON_OFFSETS, ACTIONS

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
