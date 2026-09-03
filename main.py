
import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')
import hid
import os
import fcntl
import time

VENDOR_ID = 0x258a
PRODUCT_ID = 0x002f
MODE_BYTE_OFFSET = 69
HIDIOCGFEATURE = (3 << 30) | (ord('H') << 8) | 0x07 | (154 << 16)
HIDIOCSFEATURE = (3 << 30) | (ord('H') << 8) | 0x06 | (520 << 16)


def set_mode(vendor_id: int, product_id: int, mode: int) -> None:
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
    _initialize_device(device)
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    buf[3] = 0x92  # write operation flag, required for SET_REPORT
    write_buf = buf + bytearray(520 - len(buf))
    fcntl.ioctl(device, HIDIOCSFEATURE, write_buf)


def change_color(vendor_id, product_id, colour) -> None:
    """

    :param vendor_id: vendor id
    :param product_id: product id
    :param colour: colour code
    """
    device = _build_device(vendor_id, product_id)
    buf = _get_current_state(device)


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


def _initialize_device(device) -> None:
    """
    Sends the initialization command to put the device in a receptive state.
    Must be called before reading current state.
    :param device: file descriptor for the hidraw interface
    """
    buf = bytearray(8)
    buf[0] = 0x05
    buf[1] = 0x21
    HIDIOCSFEATURE_8 = (3 << 30) | (ord('H') << 8) | 0x06 | (8 << 16)
    fcntl.ioctl(device, HIDIOCSFEATURE_8, buf)


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
            if f'0000{vendor_id:04X}:0000{product_id:04X}' in content.upper() and 'input1' in content:
                fd = open(f'/dev/{name}', 'rb+', buffering=0)
                return fd
        except FileNotFoundError:
            continue
    raise FileNotFoundError('Device not found')


def _get_current_state(device) -> bytearray:
    """
    Reads the current lighting and settings configuration from the mouse.
    Returns a 154-byte bytearray representing the full device state.
    :param device:
    """
    buf = bytearray(154)
    buf[0] = 0x08
    fcntl.ioctl(device, HIDIOCGFEATURE, buf)  # 520 bytes
    return buf



'''battery = get_battery(VENDOR_ID, PRODUCT_ID)
print(f"Battery: {battery}%")

for i in range(10):
    battery = get_battery(VENDOR_ID, PRODUCT_ID)
    print(f"Battery: {battery}%")
    set_mode(VENDOR_ID, PRODUCT_ID, i)
    time.sleep(2)
'''

if __name__ == '__main__':
    set_mode(VENDOR_ID, PRODUCT_ID, 0)
