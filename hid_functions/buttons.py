"""
Button remapping for Redragon M602KS mouse.

Supports remapping 7 buttons to 14 different actions including:
- Standard mouse clicks
- Media controls
- DPI adjustments
- RGB toggle
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

import fcntl
import os
import json

from .device import _build_device
from .constants import HIDIOCSFEATURE_520


# Configuration persistence
CONFIG_DIR = os.path.expanduser('~/.config/redragon-control')
BUTTON_CONFIG_FILE = os.path.join(CONFIG_DIR, 'button_config.json')

# Factory default button configuration
FACTORY_DEFAULT_PAYLOAD = bytearray(bytes.fromhex(
    '082200500000000011010000110200001104000011080000111000004101000041020000'
    '500400005001000050010000500100005001000050010000500100005001000050010000'
    '500100005001000050010000500100005001000050010000a500'
) + b'\x00' * (520 - 98))

# Button name to payload offset mapping
BUTTON_OFFSETS = {
    'left_click': 8,
    'right_click': 12,
    'middle_click': 16,
    'back': 20,
    'forward': 24,
    'dpi_plus': 28,
    'dpi_minus': 32,
}

# Action name to 4-byte payload mapping
ACTIONS = {
    'left_click': (17, 1, 0, 0),
    'right_click': (17, 2, 0, 0),
    'back': (17, 8, 0, 0),
    'forward': (17, 16, 0, 0),
    'middle_click': (17, 4, 0, 0),
    'three_click': (49, 1, 50, 3),
    'disable': (80, 1, 0, 0),
    'rgb_toggle': (80, 2, 0, 0),
    'dpi_plus': (65, 1, 0, 0),
    'dpi_minus': (65, 2, 0, 0),
    'dpi_loop': (65, 0, 0, 0),
    'play_pause': (34, 8, 0, 0),
    'next_track': (34, 1, 0, 0),
    'previous_track': (34, 2, 0, 0),
}


def _load_button_state() -> bytearray:
    """
    Loads button config from disk. Falls back to factory default if no saved state exists.
    
    Returns:
        bytearray: Button configuration payload
    """
    if os.path.exists(BUTTON_CONFIG_FILE):
        with open(BUTTON_CONFIG_FILE, 'r') as f:
            data = json.load(f)
        return bytearray(data['payload'])
    return FACTORY_DEFAULT_PAYLOAD.copy()


def _save_button_state(payload: bytearray) -> None:
    """
    Saves current button config to disk.
    
    Args:
        payload: Button configuration payload to save
    """
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(BUTTON_CONFIG_FILE, 'w') as f:
        json.dump({'payload': list(payload)}, f)


def set_button(vendor_id: int, product_id: int, button: str, action: str) -> None:
    """
    Assigns an action to a button and writes it to the mouse.
    
    Args:
        vendor_id: USB vendor ID (0x258a)
        product_id: USB product ID (0x002f)
        button: Button name (e.g. 'left_click', 'dpi_plus')
        action: Action name (e.g. 'right_click', 'disable')
        
    Raises:
        ValueError: If button or action name is invalid
    """
    if button not in BUTTON_OFFSETS:
        raise ValueError(f"Unknown button: {button}. Valid: {list(BUTTON_OFFSETS.keys())}")
    if action not in ACTIONS:
        raise ValueError(f"Unknown action: {action}. Valid: {list(ACTIONS.keys())}")

    payload = _load_button_state()
    offset = BUTTON_OFFSETS[button]
    payload[offset:offset + 4] = ACTIONS[action]
    _save_button_state(payload)

    device = _build_device(vendor_id, product_id)
    fcntl.ioctl(device, HIDIOCSFEATURE_520, payload)
