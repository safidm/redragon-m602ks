"""
RGB lighting control for Redragon M602KS mouse.

Supports 10 lighting modes and full RGB color customization.
Mode-specific speed, brightness, and multi-colour parameters are stored
at fixed offsets in the HID lighting report (16-byte hex-dump rows).
"""

import sys
sys.path.insert(0, '/usr/lib/python3.14/site-packages')

import fcntl

from .device import _get_current_state
from .constants import HIDIOCSFEATURE_154
from .constants import HIDIOCSFEATURE_520

REPORT_SIZE = 520
WRITE_FLAG_OFFSET = 3
WRITE_FLAG = 0x92

# 11th byte of row 0060
OFFSET_STREAMING_SPEED = 0x60 + 10
OFFSET_STEADY_BRIGHTNESS = OFFSET_STREAMING_SPEED

# Row 0070: speed in byte 1, then 7 RGB colours starting at byte 2
OFFSET_BREATHING_SPEED = 0x70
OFFSET_BREATHING_COLOURS = 0x70 + 1
BREATHING_COLOUR_COUNT = 7

# Row 0080
OFFSET_TRAIL_SPEED = 0x80 + 7          # 8th byte
OFFSET_NEON_SPEED = 0x80 + 8           # 9th byte
OFFSET_COLOURFUL_STEADY = 0x80 + 10    # 11th byte; 5 RGB slots + copy of 5th
COLOURFUL_STEADY_COLOUR_COUNT = 5

# Row 00a0
OFFSET_FLICKER_COLOURS = 133      # 10th–12th bytes, then next 3
FLICKER_COLOUR_COUNT = 2
OFFSET_STAR_TWINKLE_SPEED = 0xA0 + 15  # 16th byte

# Row 00b0
OFFSET_WAVE_SPEED = 0xB0               # 1st byte

SPEED_SLOW = 65
SPEED_MEDIUM = 66
SPEED_FAST = 67
SPEED_VALUES = (SPEED_SLOW, SPEED_MEDIUM, SPEED_FAST)

TRAIL_SPEED_SLOW = 1
TRAIL_SPEED_MEDIUM = 2
TRAIL_SPEED_FAST = 3
TRAIL_SPEED_VALUES = (TRAIL_SPEED_SLOW, TRAIL_SPEED_MEDIUM, TRAIL_SPEED_FAST)

# Highest to lowest brightness
STEADY_BRIGHTNESS_HIGHEST = 79
STEADY_BRIGHTNESS_HIGH = 63
STEADY_BRIGHTNESS_MEDIUM = 47
STEADY_BRIGHTNESS_LOW = 31
STEADY_BRIGHTNESS_VALUES = (
    STEADY_BRIGHTNESS_HIGHEST,
    STEADY_BRIGHTNESS_HIGH,
    STEADY_BRIGHTNESS_MEDIUM,
    STEADY_BRIGHTNESS_LOW,
)


def _load_report(device) -> bytearray:
    buf = bytearray(_get_current_state(device))
    if len(buf) < REPORT_SIZE:
        buf.extend(bytes(REPORT_SIZE - len(buf)))
    print(len(buf))
    return buf[:REPORT_SIZE]


def _commit_report(device, buf: bytearray) -> None:
    buf[WRITE_FLAG_OFFSET] = WRITE_FLAG
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print(f'buf{buf}')
    print(f"len: {len(buf)}")
    print(device)
    fcntl.ioctl(device, HIDIOCSFEATURE_520, buf)


def _validate_rgb(colour: tuple) -> tuple[int, int, int]:
    if colour is None or len(colour) != 3:
        raise ValueError("Colour must be an (R, G, B) tuple")
    r, g, b = colour
    for name, value in (("R", r), ("G", g), ("B", b)):
        if not isinstance(value, int) or not (0 <= value <= 255):
            raise ValueError(f"Invalid {name} value: {value}. All RGB values must be 0-255.")
    return r, g, b


def _write_bytes(device, updates: dict[int, int]) -> None:
    buf = _load_report(device)
    print(buf)
    for offset, value in updates.items():
        buf[offset] = value
    _commit_report(device, buf)


def _write_rgb(device, start: int, colour: tuple) -> None:
    r, g, b = _validate_rgb(colour)
    _write_bytes(device, {start: r, start + 1: g, start + 2: b})


def set_mode(device, mode: int) -> None:
    """
    Changes the lighting mode.

    Args:
        device: FileIO object representing the mouse
        mode: Lighting mode number (0-9)
            0: off
            1: colourful streaming
            2: steady
            3: breathing
            4: colourful tail
            5: neon
            6: colourful steady
            7: flicker
            8: star twinkle
            9: wave
    """
    MODE_BYTE_OFFSET = 69
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET] = mode
    buf[3] = 0x92  # write operation flag, required for SET_REPORT
    write_buf = buf + bytearray(520 - len(buf))
    fcntl.ioctl(device, HIDIOCSFEATURE_154, write_buf)


def set_colour(device, colour: tuple) -> None:
    """
    Sets the RGB color of the mouse lighting.

    Args:
        device: FileIO object representing the mouse
        colour: RGB tuple (r, g, b) with values 0-255
    """
    MODE_BYTE_OFFSET = (73, 74, 75)
    buf = _get_current_state(device)
    buf[MODE_BYTE_OFFSET[0]] = colour[0]
    buf[MODE_BYTE_OFFSET[1]] = colour[1]
    buf[MODE_BYTE_OFFSET[2]] = colour[2]
    buf[3] = 0x92  # write operation flag, required for SET_REPORT
    write_buf = buf + bytearray(520 - len(buf))
    fcntl.ioctl(device, HIDIOCSFEATURE_154, write_buf)


def apply_mode_settings(device, mode: int, settings: list[tuple]) -> None:
    """Applies a mode and its settings together, preserving all other bytes."""
    if mode < 0 or mode > 9:
        raise ValueError(f"Invalid lighting mode: {mode}. Valid modes are 0-9.")

    speed_offsets = {
        1: OFFSET_STREAMING_SPEED, 3: OFFSET_BREATHING_SPEED,
        4: OFFSET_TRAIL_SPEED, 5: OFFSET_NEON_SPEED,
        8: OFFSET_STAR_TWINKLE_SPEED, 9: OFFSET_WAVE_SPEED,
    }
    updates = {69: mode}
    for setting in settings:
        kind = setting[0]
        if kind == "speed":
            _, speed = setting
            if mode not in speed_offsets:
                raise ValueError(f"Lighting mode {mode} does not support speed.")
            valid_values = TRAIL_SPEED_VALUES if mode == 4 else SPEED_VALUES
            if speed not in valid_values:
                raise ValueError(f"Invalid speed: {speed}.")
            updates[speed_offsets[mode]] = speed
        elif kind == "brightness":
            _, brightness = setting
            if mode != 2 or brightness not in STEADY_BRIGHTNESS_VALUES:
                raise ValueError(f"Invalid brightness: {brightness}.")
            updates[OFFSET_STEADY_BRIGHTNESS] = brightness
        elif kind == "colour":
            _, index, colour = setting
            r, g, b = _validate_rgb(colour)
            if mode == 2:
                start = 73
            elif mode == 3:
                if index < 1 or index > BREATHING_COLOUR_COUNT:
                    raise ValueError(f"Invalid breathing colour index: {index}.")
                start = OFFSET_BREATHING_COLOURS + (index - 1) * 3
            elif mode == 6:
                if index < 1 or index > COLOURFUL_STEADY_COLOUR_COUNT:
                    raise ValueError(f"Invalid colourful steady colour index: {index}.")
                start = OFFSET_COLOURFUL_STEADY + (index - 1) * 3
                if index == COLOURFUL_STEADY_COLOUR_COUNT:
                    duplicate = OFFSET_COLOURFUL_STEADY + COLOURFUL_STEADY_COLOUR_COUNT * 3
                    updates.update({duplicate: r, duplicate + 1: g, duplicate + 2: b})
            elif mode == 7:
                if index < 1 or index > FLICKER_COLOUR_COUNT:
                    raise ValueError(f"Invalid flicker colour index: {index}.")
                start = OFFSET_FLICKER_COLOURS + (index - 1) * 3
            else:
                raise ValueError(f"Lighting mode {mode} does not support colours.")
            updates.update({start: r, start + 1: g, start + 2: b})
        else:
            raise ValueError(f"Unknown lighting setting: {kind}.")
    '''
    updates[170] = 255
    updates[171] = 0
    updates[172] = 0
    updates[173] = 0
    updates[174] = 0
    updates[175] = 255
    updates.pop(169)
    updates.pop(170)
    updates.pop(171)
    updates.pop(172)
    updates.pop(173)
    updates.pop(174)
    '''
    print(updates)
    _write_bytes(device, updates)


def set_streaming_speed(device, speed: int) -> None:
    """Sets colourful streaming speed: 65 slow, 66 medium, 67 fast."""
    if speed not in SPEED_VALUES:
        raise ValueError(f"Invalid streaming speed: {speed}. Valid values: {list(SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_STREAMING_SPEED: speed})


def set_steady_brightness(device, brightness: int) -> None:
    """Sets steady brightness: 79 highest, 63, 47, 31 lowest."""
    if brightness not in STEADY_BRIGHTNESS_VALUES:
        raise ValueError(
            f"Invalid steady brightness: {brightness}. Valid values: {list(STEADY_BRIGHTNESS_VALUES)}"
        )
    _write_bytes(device, {OFFSET_STEADY_BRIGHTNESS: brightness})


def set_breathing_speed(device, speed: int) -> None:
    """Sets breathing speed: 65 slow, 66 medium, 67 fast."""
    if speed not in SPEED_VALUES:
        raise ValueError(f"Invalid breathing speed: {speed}. Valid values: {list(SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_BREATHING_SPEED: speed})


def set_breathing_colour(device, index: int, colour: tuple) -> None:
    """
    Sets one of the 7 breathing cycle colours (1 = first colour, 7 = last).
    """
    set_breathing_colours(device, {index: colour})


def set_breathing_colours(device, colours: dict[int, tuple]) -> None:
    """Sets one or more breathing cycle colours in a single HID report."""
    updates = {}
    for index, colour in colours.items():
        if index < 1 or index > BREATHING_COLOUR_COUNT:
            raise ValueError(f"Invalid breathing colour index: {index}. Valid indices: 1-{BREATHING_COLOUR_COUNT}")
        r, g, b = _validate_rgb(colour)
        start = OFFSET_BREATHING_COLOURS + (index - 1) * 3
        updates.update({start: r, start + 1: g, start + 2: b})
    _write_bytes(device, updates)


def set_trail_speed(device, speed: int) -> None:
    """Sets colourful trail speed: 1 slow, 2 medium, 3 fast."""
    if speed not in TRAIL_SPEED_VALUES:
        raise ValueError(f"Invalid trail speed: {speed}. Valid values: {list(TRAIL_SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_TRAIL_SPEED: speed})


def set_neon_speed(device, speed: int) -> None:
    """Sets neon speed: 65 slow, 66 medium, 67 fast."""
    if speed not in SPEED_VALUES:
        raise ValueError(f"Invalid neon speed: {speed}. Valid values: {list(SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_NEON_SPEED: speed})


def set_colourful_steady_colour(device, index: int, colour: tuple) -> None:
    """
    Sets one of the 5 colourful-steady LED colours (1 = front of the mouse).

    When the 5th colour is set, the following 3 bytes are written to the same RGB.
    """
    set_colourful_steady_colours(device, {index: colour})


def set_colourful_steady_colours(device, colours: dict[int, tuple]) -> None:
    """Sets one or more colourful-steady LED colours in a single HID report."""
    updates = {}
    for index, colour in colours.items():
        if index < 1 or index > COLOURFUL_STEADY_COLOUR_COUNT:
            raise ValueError(
                f"Invalid colourful steady colour index: {index}. Valid indices: 1-{COLOURFUL_STEADY_COLOUR_COUNT}"
            )
        r, g, b = _validate_rgb(colour)
        start = OFFSET_COLOURFUL_STEADY + (index - 1) * 3
        updates.update({start: r, start + 1: g, start + 2: b})
        if index == COLOURFUL_STEADY_COLOUR_COUNT:
            dup = OFFSET_COLOURFUL_STEADY + COLOURFUL_STEADY_COLOUR_COUNT * 3
            updates.update({dup: r, dup + 1: g, dup + 2: b})
    _write_bytes(device, updates)


def set_flicker_colour(device, index: int, colour: tuple) -> None:
    """Sets one of the 2 flicker colours (1 or 2)."""
    set_flicker_colours(device, {index: colour})


def set_flicker_colours(device, colours: dict[int, tuple]) -> None:
    """Sets one or more flicker colours in a single HID report."""
    updates = {}
    for index, colour in colours.items():
        if index < 1 or index > FLICKER_COLOUR_COUNT:
            raise ValueError(f"Invalid flicker colour index: {index}. Valid indices: 1-{FLICKER_COLOUR_COUNT}")
        r, g, b = _validate_rgb(colour)
        start = OFFSET_FLICKER_COLOURS + (index - 1) * 3
        updates.update({start: r, start + 1: g, start + 2: b})
    _write_bytes(device, updates)


def set_star_twinkle_speed(device, speed: int) -> None:
    """Sets star twinkle speed: 65 slow, 66 medium, 67 fast."""
    if speed not in SPEED_VALUES:
        raise ValueError(f"Invalid star twinkle speed: {speed}. Valid values: {list(SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_STAR_TWINKLE_SPEED: speed})


def set_wave_speed(device, speed: int) -> None:
    """Sets wave speed: 65 slow, 66 medium, 67 fast."""
    if speed not in SPEED_VALUES:
        raise ValueError(f"Invalid wave speed: {speed}. Valid values: {list(SPEED_VALUES)}")
    _write_bytes(device, {OFFSET_WAVE_SPEED: speed})
