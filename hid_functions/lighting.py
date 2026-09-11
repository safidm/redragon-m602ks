"""
RGB lighting control for Redragon M602KS mouse.

Supports 10 lighting modes and full RGB color customization.
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

import fcntl

from .device import _get_current_state
from .constants import HIDIOCSFEATURE_154


def set_mode(device, mode: int) -> None:
    """
    Changes the lighting mode.
    
    Args:
        device: FileIO object representing the mouse
        mode: Lighting mode number (0-9)
            0: off
            1: steady
            2: breathing
            3: wave
            4: reactive
            5: flashing
            6: disco
            7: rainbow
            8: ripple
            9: custom
    """
    MODE_BYTE_OFFSET = 69
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    buf[3] = 0x92  # write operation flag, required for SET_REPORT
    write_buf = buf + bytearray(520 - len(buf))
    fcntl.ioctl(device, HIDIOCSFEATURE_154, write_buf)


def set_colour(device, colour: tuple) -> None:
    """
    Sets the RGB color of the mouse lighting.
    
    Args:
        device: FileIO object representing the mouse
        colour: RGB tuple (r, g, b) with values 0-255
    """
    MODE_BYTE_OFFSET = (73, 74, 75)
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET[0]] = colour[0]
    buf[MODE_BYTE_OFFSET[1]] = colour[1]
    buf[MODE_BYTE_OFFSET[2]] = colour[2]
    buf[3] = 0x92  # write operation flag, required for SET_REPORT
    write_buf = buf + bytearray(520 - len(buf))
    fcntl.ioctl(device, HIDIOCSFEATURE_154, write_buf)
