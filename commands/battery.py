"""
Battery command handler for Redragon M602KS Linux Control CLI.

This module handles battery status queries and display formatting.
"""

from main import get_battery, VENDOR_ID, PRODUCT_ID


def handle_battery(args):
    """
    Main handler for battery command.
    Calls get_battery(), formats output, and displays.

    Args:
        args: Parsed command-line arguments from argparse

    Returns:
        int: Exit code (0 for success)
    """
    percentage = get_battery(VENDOR_ID, PRODUCT_ID)

    if percentage is None:
        print("✗ Unable to read battery level")
        return 1

    display = format_battery_display(percentage)
    print(display)
    return 0


def format_battery_display(percentage: int) -> str:
    """
    Creates formatted battery display with progress bar.

    Args:
        percentage: Battery level 0-100

    Returns:
        Formatted string with progress bar, and percentage

    Example output:
        Redragon M602KS
        [████████████████████          ] 75%
    """
    progress_bar = create_progress_bar(percentage)

    return f"""🖱 Redragon M602KS
{progress_bar} {percentage}%
Status: OK"""


def create_progress_bar(percentage: int, width: int = 30) -> str:
    """
    Creates a character-based progress bar.

    Args:
        percentage: Value from 0-100
        width: Total width of progress bar in characters (default: 30)

    Returns:
        String like "[████████          ]"
    """
    filled_count = round(width * percentage / 100)
    empty_count = width - filled_count

    filled_chars = '█' * filled_count
    empty_chars = ' ' * empty_count

    return f"[{filled_chars}{empty_chars}]"
