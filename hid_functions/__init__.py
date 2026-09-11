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
from .lighting import set_mode, set_colour
from .buttons import set_button, BUTTON_OFFSETS, ACTIONS

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
