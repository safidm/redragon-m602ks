"""
Device initialization and access for Redragon M602KS mouse.

This module handles finding the correct HID interface and initializing
the device for configuration changes.
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

import os
import fcntl
import time

from .constants import HIDIOCSFEATURE_8, HIDIOCGFEATURE_154


def initialize(vendor_id: int, product_id: int):
    """
    Initializes the mouse and return a FileIO object representing the mouse device.
    
    Args:
        vendor_id: USB vendor ID (0x258a)
        product_id: USB product ID (0x002f)
        
    Returns:
        FileIO: Device file descriptor for HID communication
    """
    device = _build_device(vendor_id, product_id)
    _initialize_device(device)
    return device


def _build_device(vendor_id: int, product_id: int):
    """
    Finds and opens the correct hidraw interface for lighting control.
    Scans /sys/class/hidraw/ and matches by vendor/product ID and interface 1 (input1).
    
    Args:
        vendor_id: The USB vendor ID of the mouse
        product_id: The USB product ID of the mouse
        
    Returns:
        FileIO: File descriptor for the HID device
        
    Raises:
        FileNotFoundError: If the device is not found
    """
    for name in os.listdir('/sys/class/hidraw/'):
        uevent_path = f'/sys/class/hidraw/{name}/device/uevent'
        try:
            with open(uevent_path, 'r') as f:
                content = f.read()
            if f'0000{vendor_id:04X}:0000{product_id:04X}' in content.upper() and 'input1' in content:
                fd = open(f'/dev/{name}', 'rb+', buffering=0)
                return fd
        except FileNotFoundError:
            continue
    raise FileNotFoundError('Device not found')


def _initialize_device(device) -> None:
    """
    Sends the initialization command to put the device in a receptive state.
    Must be called before reading current state.
    
    Args:
        device: FileIO object representing the mouse
    """
    buf = bytearray(8)
    buf[0] = 0x05
    buf[1] = 0x21
    fcntl.ioctl(device, HIDIOCSFEATURE_8, buf)
    time.sleep(0.1)


def _get_current_state(device) -> bytearray:
    """
    Reads the current lighting and settings configuration from the mouse.
    Returns a 154-byte bytearray representing the full device state.
    
    Args:
        device: FileIO object representing the mouse
        
    Returns:
        bytearray: 154-byte configuration buffer
    """
    buf = bytearray(154)
    buf[0] = 0x08
    fcntl.ioctl(device, HIDIOCGFEATURE_154, buf)  # 520 bytes
    return buf
