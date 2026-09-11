# Redragon M602KS Linux Control CLI

A command-line interface for controlling the Redragon M602KS gaming mouse on Linux systems. Control battery monitoring, RGB lighting, and button mappings without needing the Windows application.

## Features

- **Battery Monitoring**: Check battery level with a visual progress bar
- **RGB Lighting Control**: 
  - 10 lighting modes (off, steady, breathing, wave, reactive, flashing, disco, rainbow, ripple, custom)
  - Custom RGB color configuration (16.7 million colors)
- **Button Remapping**: View button assignments and available actions
- **User-Friendly**: Clear error messages, helpful examples, consistent output formatting

## Requirements

- **Operating System**: Linux (tested on Fedora)
- **Python**: Python 3.14 or higher
- **Dependencies**: `hid` library for USB HID communication
- **Hardware**: Redragon M602KS mouse connected via USB-C cable or 2.4G wireless receiver

## Installation

1. Clone or download this repository
2. Install the required Python library:

```bash
pip install hid==1.0.6
```

3. **(Optional)** Set up udev rules to run without sudo:

```bash
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="258a", MODE="0666"' | sudo tee /etc/udev/rules.d/50-redragon.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

After setting up the udev rule, unplug and replug your mouse, then you can run commands without `sudo`.

## Usage

### Check Battery Status

```bash
python3 cli.py battery
```

Output:
```
🖱 Redragon M602KS
[████████████████░░░░░░░░░░░░░░] 62%
Status: OK
```

### Lighting Control

#### List Available Lighting Modes

```bash
python3 cli.py lighting mode
```

Output shows all 10 modes with descriptions:
```
Available lighting modes:
  0: off        - Turns off all lighting
  1: steady     - Solid constant color
  2: breathing  - Smooth fade in and out
  3: wave       - Color wave effect
  4: reactive   - Responds to clicks
  5: flashing   - Quick on/off pulses
  6: disco      - Random color changes
  7: rainbow    - Cycling rainbow effect
  8: ripple     - Ripple effect from center
  9: custom     - User-defined pattern
```

#### Set Lighting Mode

```bash
python3 cli.py lighting mode 2
```

Output:
```
✓ Lighting mode set to: breathing
```

#### Show Color Usage Examples

```bash
python3 cli.py lighting color
```

Output:
```
Usage: python3 cli.py lighting color <R> <G> <B>
R, G, B values must be between 0 and 255.

Examples:
  Red:    python3 cli.py lighting color 255 0 0
  Green:  python3 cli.py lighting color 0 255 0
  Blue:   python3 cli.py lighting color 0 0 255
  White:  python3 cli.py lighting color 255 255 255
  Off:    python3 cli.py lighting color 0 0 0
```

#### Set Custom RGB Color

```bash
python3 cli.py lighting color 255 0 0
```

Output:
```
✓ Color set to: R=255 G=0 B=0 (red)
```

### Button Control

#### View Button Assignments

```bash
python3 cli.py buttons
```

Output shows current assignments and available actions:
```
Current Button Assignments:
  left_click      → left_click
  right_click     → right_click
  middle_click    → middle_click
  back            → back
  forward         → forward
  dpi_plus        → dpi_plus
  dpi_minus       → dpi_minus

Available Actions:
  left_click        Standard left mouse button
  right_click       Standard right mouse button
  middle_click      Standard middle mouse button
  back              Browser back button
  forward           Browser forward button
  three_click       Simulates three rapid clicks
  disable           Disables the button
  rgb_toggle        Toggles RGB lighting on/off
  dpi_plus          Increases DPI sensitivity
  dpi_minus         Decreases DPI sensitivity
  dpi_loop          Cycles through DPI presets
  play_pause        Media play/pause control
  next_track        Skip to next media track
  previous_track    Skip to previous media track
```

#### Remap a Button

```bash
python3 cli.py buttons set dpi_minus play_pause
```

Output:
```
✓ dpi_minus button set to: play_pause

⚠ Note: Button remapping requires HID layer support (not yet implemented)
```

### Sensitivity Control

```bash
python3 cli.py sensitivity
```

Output:
```
⚠ Sensitivity control coming soon.
```


## Limitations

- **Windows Application Incompatibility**: Setting custom macros through this CLI will not be reflected in the official Windows application, and vice versa. The mouse stores settings independently, so changes made on Linux won't sync with Windows configuration profiles. THIS IS ONLY THE CASE FOR CUSTOM MACROS.

- **Battery Reading Fluctuation**: The battery percentage may fluctuate by ±2% between readings due to hardware reporting variations. This is normal behavior.

## Project Structure

```
redragon-m602ks/
├── cli.py                  # CLI entry point with argument parser
├── commands/               # Command handler modules
│   ├── __init__.py
│   ├── battery.py          # Battery status display
│   ├── lighting.py         # Lighting mode and color control
│   ├── buttons.py          # Button remapping
│   └── sensitivity.py      # Sensitivity control placeholder
├── hid/                    # Hardware interface layer
│   ├── __init__.py         # Public API
│   ├── constants.py        # USB IDs and constants
│   ├── device.py           # Device initialization
│   ├── battery.py          # Battery monitoring
│   ├── lighting.py         # RGB lighting control
│   └── buttons.py          # Button remapping logic
├── main.py                 # Backwards compatibility shim
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## License

This project is provided as-is for personal use. It is not affiliated with or endorsed by Redragon.
