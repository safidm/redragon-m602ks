
import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')
import hid
import os
import fcntl

VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f
MODE_BYTE_OFFSET = 69
HIDIOCGFEATURE = 0xc2084807  # set state command
HIDIOCSFEATURE = 0xc2084806  # get state command


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
    currently broken
    Builds a __ to get the bytes for the lighting
    :param vendor_id: the vendor id of the mouse
    :param product_id: the product id of the mouse
    """
    target = None
    devices = os.listdir('/sys/class/hidraw/')
    for i in range(len(devices)):
        path = os.readlink('/sys/class/hidraw/' + devices[i])
        if f'{vendor_id:04X}:{product_id:04X}' in path.upper() and '1.0' in path:
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


def get_current_state(device) -> bytearray:
    """
    Reads the current lighting and settings configuration from the mouse.
    Returns a 520-byte bytearray representing the full device state,
    :param device:
    :return:
    """
    buf = bytearray(520)
    buf[0] = 0x08
    fcntl.ioctl(device, HIDIOCGFEATURE, buf)
    return buf


def set_mode(device, mode: int) -> None:
    """
    Changes the lighting mode to one of the following:
    0:
    1:
    2:
    3:
    4:
    5:
    6:
    7:
    8:
    9:
    :param device:
    :param mode:
    """
    buf = get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    fcntl.ioctl(device, HIDIOCSFEATURE, buf)


'''dev = build_device_battery(VENDOR_ID, PRODUCT_ID)
get_battery(dev)
'''

dev = open('/dev/hidraw5', 'rb+', buffering=0)

set_mode(dev, 6)
