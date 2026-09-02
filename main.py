
import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')
from io import FileIO
import hid
import os
import fcntl
import struct



def build_device_battery(vendor_id: int, product_id: int) -> hid.device:
    """
    Builds a hid.device object for the get_battery function
    :param vendor_id:
    :param product_id:
    :return:
    """
    devices = hid.enumerate(vendor_id, product_id)
    target = None
    for d in devices:
        if d['usage_page'] == 0xFF00:
            target = d
            break
    dev = hid.Device(path=target['path'])
    return dev


def build_device(vendor_id: int, product_id: int) -> None | FileIO:
    """
    Builds a __ to get the bytes for the lighting
    :param vendor_id: the vendor id of the mouse
    :param product_id: the product id of the mouse
    """
    target = None
    devices = os.listdir('/sys/class/hidraw/')
    for i in range(len(devices)):
        path = os.readlink('/sys/class/hidraw/' + devices[i])
        if f'{vendor_id:04X}:{product_id:04X}' in path.upper() and '1.1' in path:
            target = f'/dev/{devices[i]}'
            break
    if target is None:
        raise FileNotFoundError
    print(open(target, 'rb+', buffering=0))
    return open(target, 'rb+', buffering=0)


def get_battery(device: hid.device) -> int:
    """
    :param device: a hid object respresenting the mouse
    :return: integer indicating the battery life
    """
    response = device.get_feature_report(0x05, 8)

    # parsing the response to get the right byte
    raw_byte = None
    for i in range(len(response) - 3):
        if response[i] == 0x05 and response[i + 1] == 0x90 and response[i + 2] == 0x11:
            raw_byte = response[i + 3]
    print(raw_byte, '%')
    return raw_byte


def set_mode(device: hid.device) -> None:
    """
    :param device: a hid object respresenting the mouse
    :return: None
    """
    #to be implemented

VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f


dev = build_device_battery(VENDOR_ID, PRODUCT_ID)
get_battery(dev)


dev = build_device(VENDOR_ID, PRODUCT_ID)


size = 520
HIDIOCGFEATURE = (0xC0000000 | (size << 16) | (0x48 << 8) | 0x07)
print(hex(HIDIOCGFEATURE))
