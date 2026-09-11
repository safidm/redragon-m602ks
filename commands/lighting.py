"""
Lighting command handler for Redragon M602KS Linux Control CLI.

This module handles lighting mode and color control.
"""

from main import initialize, set_mode, VENDOR_ID, PRODUCT_ID

# Lighting modes with names and descriptions
LIGHTING_MODES = {
    0: ("off", "Turns off all lighting"),
    1: ("steady", "Solid constant color"),
    2: ("breathing", "Smooth fade in and out"),
    3: ("wave", "Color wave effect"),
    4: ("reactive", "Responds to clicks"),
    5: ("flashing", "Quick on/off pulses"),
    6: ("disco", "Random color changes"),
    7: ("rainbow", "Cycling rainbow effect"),
    8: ("ripple", "Ripple effect from center"),
    9: ("custom", "User-defined pattern")
}


def handle_lighting(args):
    """
    Main handler for lighting command.
    Routes to mode or color handlers based on subcommand.
    
    Args:
        args: Parsed command-line arguments from argparse
        
    Returns:
        int: Exit code (0 for success)
    """
    if args.lighting_subcommand == "mode":
        return handle_mode(args)
    elif args.lighting_subcommand == "color":
        return handle_color(args)
    else:
        # Default to showing help
        print("Please specify a subcommand: mode or color")
        return 0


def handle_mode(args):
    """
    Handler for lighting mode subcommand.
    If mode argument provided: set the mode
    If no argument: display available modes
    
    Args:
        args: Parsed command-line arguments with optional mode_number attribute
        
    Returns:
        int: Exit code (0 for success)
    """
    if hasattr(args, 'mode_number') and args.mode_number is not None:
        # Validate mode number
        if args.mode_number < 0 or args.mode_number > 9:
            raise ValueError(
                f"Invalid mode: {args.mode_number}. Valid modes are 0-9.\n"
                "Run 'python3 cli.py lighting mode' to see available modes."
            )
        set_lighting_mode(args.mode_number)
    else:
        display_modes()
    return 0


def display_modes():
    """
    Displays all 10 lighting modes with numeric IDs and descriptions.
    """
    print("Available lighting modes:")
    for mode_id in sorted(LIGHTING_MODES.keys()):
        name, description = LIGHTING_MODES[mode_id]
        print(f"  {mode_id}: {name:<10} - {description}")


def set_lighting_mode(mode: int):
    """
    Initializes device and calls set_mode.
    Displays success message with mode name.
    
    Args:
        mode: Lighting mode number (0-9)
    """
    device = initialize(VENDOR_ID, PRODUCT_ID)
    set_mode(device, mode)
    mode_name = LIGHTING_MODES[mode][0]
    print(f"✓ Lighting mode set to: {mode_name}")


# Common colors for recognition
COMMON_COLORS = {
    (255, 0, 0): "red",
    (0, 255, 0): "green",
    (0, 0, 255): "blue",
    (255, 255, 255): "white",
    (0, 0, 0): "off"
}


def handle_color(args):
    """
    Handler for lighting color subcommand.
    If RGB arguments provided: set the color
    If no arguments: display usage and examples
    
    Args:
        args: Parsed command-line arguments with optional r, g, b attributes
        
    Returns:
        int: Exit code (0 for success)
    """
    # Check if RGB values were provided
    if hasattr(args, 'r') and args.r is not None:
        # All RGB values should be provided if r is provided
        if args.g is None or args.b is None:
            display_color_usage()
            return 0
        
        set_lighting_color(args.r, args.g, args.b)
    else:
        # No arguments - display usage
        display_color_usage()
    
    return 0


def display_color_usage():
    """
    Displays color command usage with RGB constraints and 5 examples.
    """
    print("Usage: python3 cli.py lighting color <R> <G> <B>")
    print("R, G, B values must be between 0 and 255.")
    print()
    print("Examples:")
    print("  Red:    python3 cli.py lighting color 255 0 0")
    print("  Green:  python3 cli.py lighting color 0 255 0")
    print("  Blue:   python3 cli.py lighting color 0 0 255")
    print("  White:  python3 cli.py lighting color 255 255 255")
    print("  Off:    python3 cli.py lighting color 0 0 0")


def set_lighting_color(r: int, g: int, b: int):
    """
    Validates RGB range, initializes device, calls set_colour.
    Displays success message with RGB values and color name if recognized.
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Raises:
        ValueError: If any RGB value is out of range
    """
    # Validate RGB range
    if not (0 <= r <= 255):
        raise ValueError(
            f"Invalid RGB value: {r}. All RGB values must be 0-255.\n"
            "Run 'python3 cli.py lighting color' for usage and examples."
        )
    if not (0 <= g <= 255):
        raise ValueError(
            f"Invalid RGB value: {g}. All RGB values must be 0-255.\n"
            "Run 'python3 cli.py lighting color' for usage and examples."
        )
    if not (0 <= b <= 255):
        raise ValueError(
            f"Invalid RGB value: {b}. All RGB values must be 0-255.\n"
            "Run 'python3 cli.py lighting color' for usage and examples."
        )
    
    # Import set_colour from main
    from main import set_colour
    
    # Initialize device and set color
    device = initialize(VENDOR_ID, PRODUCT_ID)
    set_colour(device, (r, g, b))
    
    # Build success message
    color_name = get_color_name(r, g, b)
    if color_name:
        print(f"✓ Color set to: R={r} G={g} B={b} ({color_name})")
    else:
        print(f"✓ Color set to: R={r} G={g} B={b}")


def get_color_name(r: int, g: int, b: int) -> str | None:
    """
    Returns human-readable name for common colors.
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Returns:
        str: Color name if recognized, None otherwise
    """
    return COMMON_COLORS.get((r, g, b))
