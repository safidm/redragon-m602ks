"""
USB constants and hardware identifiers for Redragon M602KS mouse.

This module defines USB vendor/product IDs and HID ioctl command constants
used for communication with the mouse.
"""

# USB device identifiers
VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f

# ioctl command for setting HID feature report
HIDIOCSFEATURE = lambda size: (3 << 30) | (ord('H') << 8) | 0x06 | (size << 16)
HIDIOCSFEATURE_8 = HIDIOCSFEATURE(8)
HIDIOCSFEATURE_154 = (3 << 30) | (ord('H') << 8) | 0x06 | (520 << 16)  # For write operations
HIDIOCSFEATURE_520 = HIDIOCSFEATURE(520)

# ioctl command for getting HID feature report
HIDIOCGFEATURE = lambda size: (3 << 30) | (ord('H') << 8) | 0x07 | (size << 16)
HIDIOCGFEATURE_154 = HIDIOCGFEATURE(154)
