
import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')
import hid
import os
import fcntl
import time

VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f
MODE_BYTE_OFFSET = 69
HIDIOCGFEATURE = 0xc2084807  # get state command
HIDIOCSFEATURE = 0xc2084806  # set state command

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
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    fcntl.ioctl(device, HIDIOCSFEATURE, buf)


def get_battery(vendor_id: int, product_id: int) -> int | None:
    """
    Returns an integer indicating the battery life
    :param vendor_id: vendor id
    :param product_id: product id
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
        try:
            with open(uevent_path, 'r') as f:
                content = f.read()
            if f'0000{vendor_id:04X}:0000{product_id:04X}' in content.upper() and 'input0' in content:
                return open(f'/dev/{name}', 'rb+', buffering=0)
        except FileNotFoundError:
            continue
    raise FileNotFoundError('Device not found')


def _get_current_state(device) -> bytearray:
    """
    Reads the current lighting and settings configuration from the mouse.
    Returns a 520-byte bytearray representing the full device state.
    :param device:
    """
    buf = bytearray(520)
    buf[0] = 0x08
    fcntl.ioctl(device, HIDIOCGFEATURE, buf)
    return buf


battery = get_battery(VENDOR_ID, PRODUCT_ID)
print(f"Battery: {battery}%")
