
import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')
import hid
import os
import fcntl

VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f
MODE_BYTE_OFFSET = 69
HIDIOCGFEATURE = 0xc2084807  # get state command
HIDIOCSFEATURE = 0xc2084806  # set state command


def _build_device_battery(vendor_id: int, product_id: int) -> hid.device:
    """
    Returns a hid.device object for the get_battery function
    :param vendor_id: vendor id
    :param product_id: product id
    """
    devices = hid.enumerate(vendor_id, product_id)
    target = None
    for d in devices:
        if d['usage_page'] == 0xFF00:
            target = d
            break
    device = hid.Device(path=target['path'])
    return device


def _build_device(vendor_id: int, product_id: int):
    """
    Finds and opens the correct hidraw interface for lighting control.
    Scans /sys/class/hidraw/ and matches by vendor/product ID and interface 1 (input1).
    Returns a file descriptor for the hidraw interface.
    :param vendor_id: the vendor id of the mouse
    :param product_id: the product id of the mouse
    """
    for name in os.listdir('/sys/class/hidraw/'):
        uevent_path = f'/sys/class/hidraw/{name}/device/uevent'
        print(uevent_path)
        try:
            with open(uevent_path, 'r') as f:
                content = f.read()
            if f'0000{vendor_id:04X}:0000{product_id:04X}' in content.upper() and 'input1' in content:
                return open(f'/dev/{name}', 'rb+', buffering=0)
        except FileNotFoundError:
            continue
    raise FileNotFoundError('Device not found')


def get_battery(vendor_id: int, product_id: int) -> int:
    """
    Returns an integer indicating the battery life
    :param vendor_id: vendor id
    :param product_id: product id
    """
    device = _build_device_battery(vendor_id, product_id)
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
    Returns a 520-byte bytearray representing the full device state.
    :param device:
    """
    buf = bytearray(520)
    buf[0] = 0x08
    fcntl.ioctl(device, HIDIOCGFEATURE, buf)
    return buf


def set_mode(vendor_id, product_id, mode: int) -> None:
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
    :param vendor_id:
    :param product_id:
    :param mode:
    """
    device = _build_device(vendor_id, product_id)
    buf = get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    fcntl.ioctl(device, HIDIOCSFEATURE, buf)


get_battery(VENDOR_ID, PRODUCT_ID)

set_mode(VENDOR_ID, PRODUCT_ID, 4)
