import sys
from io import FileIO

import hid
import os
import fcntl
sys.path.insert(0, '/usr/lib/python3.14/site-packages')


def build_device(vendor_id: int, product_id: int) -> None | FileIO:
    """
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

dev = build_device(VENDOR_ID, PRODUCT_ID)
get_battery(dev)


# current = dev.get_feature_report(0x08, 528)
