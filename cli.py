#!/usr/bin/env python3
"""
Command-line interface for Redragon M602KS mouse control.

This CLI provides user-friendly commands for battery monitoring, lighting control,
and button remapping on Linux systems.
"""

import argparse
import sys


def setup_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the main argument parser with all subparsers.

    Returns:
        ArgumentParser: Configured ArgumentParser instance with subparsers for
                       battery, lighting, buttons, and sensitivity commands.
    """
    # Main parser
    main_parser = argparse.ArgumentParser(
        prog='cli.py',
        description='Control the Redragon M602KS gaming mouse on Linux',
        epilog='For command-specific help, use: python3 cli.py <command> --help'
    )

    # Create subparsers for commands
    subparsers = main_parser.add_subparsers(
        dest='command',
        title='Available commands',
        description='Control different aspects of the Redragon M602KS mouse',
        help='Command category'
    )

    # Battery subparser
    battery_parser = subparsers.add_parser(
        'battery',
        help='Check battery status',
        description='Display the current battery level with a progress bar'
    )

    # Lighting subparser
    lighting_parser = subparsers.add_parser(
        'lighting',
        help='Control RGB lighting',
        description='List lighting modes, inspect a mode\'s options, then apply actions'
    )
    lighting_parser.add_argument(
        'mode',
        nargs='?',
        help='Mode number (0-9) or name. Omit to list available modes.'
    )
    lighting_parser.add_argument(
        'actions',
        nargs='*',
        help='One or more actions for that mode, e.g. speed slow colour 1 red'
    )

    # Buttons subparser
    buttons_parser = subparsers.add_parser(
        'buttons',
        help='Configure button mappings',
        description='View or change button assignments'
    )

    # Buttons subcommands
    buttons_subparsers = buttons_parser.add_subparsers(
        dest='buttons_subcommand',
        title='Button commands',
        help='Button configuration options'
    )

    # Buttons set subcommand
    set_parser = buttons_subparsers.add_parser(
        'set',
        help='Remap a button to an action',
        description='Assign a new action to a button'
    )
    set_parser.add_argument(
        'button',
        type=str,
        help='Button name (e.g., back, forward, dpi_plus)'
    )
    set_parser.add_argument(
        'action',
        type=str,
        help='Action to assign (e.g., next_track, play_pause, dpi_loop)'
    )

    # Sensitivity subparser
    sensitivity_parser = subparsers.add_parser(
        'sensitivity',
        help='Adjust DPI sensitivity (coming soon)',
        description='Control mouse sensitivity settings'
    )

    return main_parser


def main() -> int:
    """
    Main entry point. Sets up argument parser, routes to command handlers,
    and catches exceptions.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        # Set up argument parser
        parser = setup_parser()
        args = parser.parse_args()

        # If no command specified, show help
        if args.command is None:
            parser.print_help()
            return 0

        # Import command handlers (lazy import to avoid loading HID layer unnecessarily)
        from commands import handle_battery, handle_lighting, handle_buttons, handle_sensitivity

        # Route to appropriate command handler
        if args.command == 'battery':
            return handle_battery(args)
        elif args.command == 'lighting':
            return handle_lighting(args)
        elif args.command == 'buttons':
            return handle_buttons(args)
        elif args.command == 'sensitivity':
            return handle_sensitivity(args)
        else:
            # This should never happen if parser is configured correctly
            parser.print_help()
            return 1

    except FileNotFoundError:
        print("✗ Mouse not found. Make sure it is plugged in and try again.")
        return 1

    except PermissionError:
        print("✗ Permission denied. Run with sudo or install the udev rule (see README).")
        return 1

    except ValueError as e:
        print(f"✗ {str(e)}")
        return 2

    except KeyboardInterrupt:
        print("\n✗ Operation cancelled by user.")
        return 130

    except Exception as e:
        print(f"✗ An unexpected error occurred: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
