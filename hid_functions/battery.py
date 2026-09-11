"""
Battery monitoring for Redragon M602KS mouse.

Reads battery level via HID feature reports when in wireless mode.
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

import hid
import time


def get_battery(vendor_id: int, product_id: int) -> int | None:
    """
    Returns an integer indicating the battery life.
    
    Args:
        vendor_id: USB vendor ID (0x258a)
        product_id: USB product ID (0x002f)
        
    Returns:
        int | None: Battery percentage (0-100) or None if unable to read
    """
    devices = hid.enumerate(vendor_id, product_id)
    for d in devices:
        try:
            dev = hid.Device(path=d['path'])
            dev.send_feature_report(bytes([0x05, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
            time.sleep(0.15)
            response = dev.get_feature_report(0x05, 8)
            dev.close()
            if response[1] == 0x90:
                return response[3]
        except Exception as e:
            if 'Broken pipe' not in str(e):
                print(e)
            continue
    return None
