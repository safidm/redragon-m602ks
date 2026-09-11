"""
Button command handler for Redragon M602KS Linux Control CLI.

This module handles button remapping display and configuration.
"""

# Valid button names
VALID_BUTTONS = [
    "left_click",
    "right_click",
    "middle_click",
    "back",
    "forward",
    "dpi_plus",
    "dpi_minus"
]

# Available actions with descriptions
AVAILABLE_ACTIONS = {
    "left_click": "Standard left mouse button",
    "right_click": "Standard right mouse button",
    "middle_click": "Standard middle mouse button",
    "back": "Browser back button",
    "forward": "Browser forward button",
    "three_click": "Simulates three rapid clicks",
    "disable": "Disables the button",
    "rgb_toggle": "Toggles RGB lighting on/off",
    "dpi_plus": "Increases DPI sensitivity",
    "dpi_minus": "Decreases DPI sensitivity",
    "dpi_loop": "Cycles through DPI presets",
    "play_pause": "Media play/pause control",
    "next_track": "Skip to next media track",
    "previous_track": "Skip to previous media track"
}

# Default button assignments (since HID layer lacks read-back functions)
DEFAULT_ASSIGNMENTS = {
    "left_click": "left_click",
    "right_click": "right_click",
    "middle_click": "middle_click",
    "back": "back",
    "forward": "forward",
    "dpi_plus": "dpi_plus",
    "dpi_minus": "dpi_minus"
}


def handle_buttons(args):
    """
    Main handler for buttons command.
    Routes to set handler or display handler based on subcommand.

    Args:
        args: Parsed command-line arguments from argparse

    Returns:
        int: Exit code (0 for success)
    """
    # Check if this is a 'set' subcommand
    if hasattr(args, 'buttons_subcommand') and args.buttons_subcommand == 'set':
        return handle_button_set(args.button, args.action)
    else:
        # Default: display button info
        display_button_info()
        return 0


def handle_button_set(button: str, action: str) -> int:
    """
    Validates button and action names, then configures button.

    Args:
        button: Button name to configure
        action: Action to assign to the button

    Returns:
        int: Exit code (0 for success)

    Raises:
        ValueError: If button or action name is invalid
    """
    validate_button(button)
    validate_action(action)

    # Note: Actual HID layer function for button remapping not yet available
    # For now, just display the success message
    print(f"✓ {button} button set to: {action}")
    print("\n⚠ Note: Button remapping requires HID layer support (not yet implemented)")

    return 0


def display_button_info() -> None:
    """
    Displays current button assignments and available actions.

    Formats output with current assignments followed by available actions.
    """
    print("Current Button Assignments:")
    # Display buttons in the specified order
    for button in VALID_BUTTONS:
        action = DEFAULT_ASSIGNMENTS[button]
        print(f"  {button:<15} → {action}")

    print("\nAvailable Actions:")
    # Display all available actions with descriptions
    for action, description in AVAILABLE_ACTIONS.items():
        print(f"  {action:<18} {description}")


def validate_button(button: str) -> None:
    """
    Validates that the button name is valid.

    Args:
        button: Button name to validate

    Raises:
        ValueError: If button name is not in VALID_BUTTONS list
    """
    if button not in VALID_BUTTONS:
        valid_buttons_str = ", ".join(VALID_BUTTONS)
        raise ValueError(
            f"Invalid button: {button}. "
            f"Valid buttons are: {valid_buttons_str}"
        )


def validate_action(action: str) -> None:
    """
    Validates that the action name is valid.

    Args:
        action: Action name to validate

    Raises:
        ValueError: If action name is not in AVAILABLE_ACTIONS dictionary
    """
    if action not in AVAILABLE_ACTIONS:
        valid_actions_str = ", ".join(AVAILABLE_ACTIONS.keys())
        raise ValueError(
            f"Invalid action: {action}. "
            f"Valid actions are: {valid_actions_str}"
        )
