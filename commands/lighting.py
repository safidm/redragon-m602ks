"""
Lighting command handler for Redragon M602KS Linux Control CLI.

This module handles lighting mode and colour control.
"""

from main import initialize, set_mode, VENDOR_ID, PRODUCT_ID

# Lighting modes with names and descriptions
LIGHTING_MODES = {
    0: ("off", "Turns off all lighting"),
    1: ("colourful streaming", "Colours smoothly changing"),
    2: ("steady", "Solid constant colour"),
    3: ("breathing", "Cycles through colours with a slow fade in/out"),
    4: ("colourful tail", "Colour changes from the front to the back of the mouse"),
    5: ("neon", "Slowly transitions between colours"),
    6: ("colourful steady", "Steady stream of multiple colours"),
    7: ("flicker", "Rapidly changes between different colours"),
    8: ("star twinkle", "Randomly switches to colours in different parts of the mouse"),
    9: ("wave", "Constantly changing steady stream of multiple colours")
}

MODE_ALIASES = {
    "off": 0,
    "streaming": 1,
    "colourful-streaming": 1,
    "colourful_streaming": 1,
    "steady": 2,
    "breathing": 3,
    "tail": 4,
    "trail": 4,
    "colourful-tail": 4,
    "colourful_tail": 4,
    "neon": 5,
    "colourful-steady": 6,
    "colourful_steady": 6,
    "flicker": 7,
    "twinkle": 8,
    "star-twinkle": 8,
    "star_twinkle": 8,
    "wave": 9,
}

# speed: None | "standard" (65/66/67) | "trail" (1/2/3)
# color_slots: 0 = none, 1 = single RGB, >1 = indexed slots
MODE_CAPABILITIES = {
    0: {"actions": ("set",), "speed": None, "brightness": False, "color_slots": 0},
    1: {"actions": ("speed",), "speed": "standard", "brightness": False, "color_slots": 0},
    2: {"actions": ("brightness", "colour"), "speed": None, "brightness": True, "color_slots": 1},
    3: {"actions": ("speed", "colour"), "speed": "standard", "brightness": False, "color_slots": 7},
    4: {"actions": ("speed",), "speed": "trail", "brightness": False, "color_slots": 0},
    5: {"actions": ("speed",), "speed": "standard", "brightness": False, "color_slots": 0},
    6: {"actions": ("colour",), "speed": None, "brightness": False, "color_slots": 5},
    7: {"actions": ("colour",), "speed": None, "brightness": False, "color_slots": 2},
    8: {"actions": ("speed",), "speed": "standard", "brightness": False, "color_slots": 0},
    9: {"actions": ("speed",), "speed": "standard", "brightness": False, "color_slots": 0},
}

NAMED_COLOURS = {
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "purple": (128, 0, 128),
    "pink": (255, 105, 180),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}

COMMON_COLORS = {rgb: name for name, rgb in NAMED_COLOURS.items()}

SPEED_65 = {
    "slow": 65,
    "medium": 66,
    "fast": 67,
    "65": 65,
    "66": 66,
    "67": 67,
}

TRAIL_SPEED = {
    "slow": 1,
    "medium": 2,
    "fast": 3,
    "1": 1,
    "2": 2,
    "3": 3,
}

BRIGHTNESS_LEVELS = {
    "highest": 79,
    "high": 63,
    "medium": 47,
    "low": 31,
    "79": 79,
    "63": 63,
    "47": 47,
    "31": 31,
}

SPEED_65_LABELS = {65: "slow", 66: "medium", 67: "fast"}
TRAIL_SPEED_LABELS = {1: "slow", 2: "medium", 3: "fast"}
BRIGHTNESS_LABELS = {79: "highest", 63: "high", 47: "medium", 31: "low"}


def handle_lighting(args):
    """
    Main handler for lighting command.

    lighting            -> list modes
    lighting <mode>     -> list that mode's actions
    lighting <mode> ... -> set the mode and apply actions
    """
    if getattr(args, "mode", None) is None:
        display_modes()
        return 0

    mode = resolve_mode(args.mode)
    actions = list(getattr(args, "actions", None) or [])
    if not actions:
        display_mode_options(mode)
        return 0

    return apply_mode_actions(mode, actions)


def handle_mode(args):
    """
    Handler for lighting mode listing / direct mode set (used by tests).
    """
    if hasattr(args, 'mode_number') and args.mode_number is not None:
        if args.mode_number < 0 or args.mode_number > 9:
            raise ValueError(
                f"Invalid mode: {args.mode_number}. Valid modes are 0-9.\n"
                "Run 'python3 cli.py lighting' to see available modes."
            )
        set_lighting_mode(args.mode_number)
    else:
        display_modes()
    return 0


def resolve_mode(token) -> int:
    raw = str(token).strip().lower().replace(" ", "-")
    if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
        mode = int(raw)
        if mode < 0 or mode > 9:
            raise ValueError(
                f"Invalid mode: {token}. Valid modes are 0-9.\n"
                "Run 'python3 cli.py lighting' to see available modes."
            )
        return mode
    if raw in MODE_ALIASES:
        return MODE_ALIASES[raw]
    raise ValueError(
        f"Invalid mode: {token}. Valid modes are 0-9.\n"
        "Run 'python3 cli.py lighting' to see available modes."
    )


def display_modes():
    """
    Displays all 10 lighting modes with numeric IDs and descriptions.
    """
    print("Available lighting modes:")
    for mode_id in sorted(LIGHTING_MODES.keys()):
        name, description = LIGHTING_MODES[mode_id]
        print(f"  {mode_id}: {name:<22} - {description}")
    print()
    print("Next step:")
    print("  python3 cli.py lighting <mode>")
    print("shows the actions available for that mode.")


def display_common_colours():
    print("Common colours:")
    for name, (r, g, b) in NAMED_COLOURS.items():
        print(f"  {name:<8}  {r:>3} {g:>3} {b:>3}")
    print("You can also pass raw RGB values (0-255), e.g. colour 255 128 0")


def display_mode_options(mode: int):
    name, description = LIGHTING_MODES[mode]
    caps = MODE_CAPABILITIES[mode]
    print(f"Mode {mode}: {name}")
    print(description)
    print()
    print("Available actions:")

    examples = []
    if "set" in caps["actions"] and len(caps["actions"]) == 1:
        print("  set                 Turn this mode on (no extra settings)")
        examples.append(f"python3 cli.py lighting {mode} set")
    if caps["speed"] == "standard":
        print("  speed <value>       slow | medium | fast")
        examples.append(f"python3 cli.py lighting {mode} speed medium")
    if caps["speed"] == "trail":
        print("  speed <value>       slow | medium | fast")
        examples.append(f"python3 cli.py lighting {mode} speed fast")
    if caps["brightness"]:
        print("  brightness <level>  highest | high | medium | low")
        examples.append(f"python3 cli.py lighting {mode} brightness high")
    if caps["color_slots"] == 1:
        print("  colour <name|R G B> Set the lighting colour")
        examples.append(f"python3 cli.py lighting {mode} colour red")
        examples.append(f"python3 cli.py lighting {mode} brightness high colour white")
    elif caps["color_slots"] > 1:
        slots = caps["color_slots"]
        extra = ""
        if mode == 6:
            extra = " (1 = front of the mouse; slot 5 is copied to the following 3 bytes)"
        elif mode == 3:
            extra = " (1 = first colour in the cycle)"
        print(f"  colour <1-{slots}> <name|R G B> Set one colour slot{extra}")
        examples.append(f"python3 cli.py lighting {mode} colour 1 red")
        if caps["speed"]:
            examples.append(f"python3 cli.py lighting {mode} speed slow colour 1 blue colour 2 green")
        else:
            examples.append(f"python3 cli.py lighting {mode} colour 1 red colour 2 blue")

    print()
    print("Command structure:")
    print(f"  python3 cli.py lighting {mode} action [action2 action3 ...]")
    print()
    print("Examples:")
    for example in examples:
        print(f"  {example}")

    if caps["color_slots"]:
        print()
        display_common_colours()


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


def parse_colour_tokens(tokens):
    """Returns ((r, g, b), tokens_consumed)."""
    if not tokens:
        raise ValueError(
            "Expected a colour name or R G B values.\n"
            "Common colours: " + ", ".join(NAMED_COLOURS)
        )
    name = tokens[0].lower()
    if name in NAMED_COLOURS:
        return NAMED_COLOURS[name], 1
    if len(tokens) < 3:
        raise ValueError(
            f"Unknown colour '{tokens[0]}'. Use a name or R G B values (0-255).\n"
            "Common colours: " + ", ".join(NAMED_COLOURS)
        )
    try:
        r, g, b = int(tokens[0]), int(tokens[1]), int(tokens[2])
    except ValueError:
        raise ValueError(
            f"Unknown colour '{tokens[0]}'. Use a name or R G B values (0-255).\n"
            "Common colours: " + ", ".join(NAMED_COLOURS)
        )
    for value in (r, g, b):
        if not (0 <= value <= 255):
            raise ValueError(f"Invalid RGB value: {value}. All RGB values must be 0-255.")
    return (r, g, b), 3


def parse_actions(mode: int, tokens):
    caps = MODE_CAPABILITIES[mode]
    allowed = set(caps["actions"]) | {"set", "apply"}
    parsed = []
    i = 0
    while i < len(tokens):
        action = tokens[i].lower()
        if action == "color":
            action = "colour"

        if action in ("set", "apply"):
            parsed.append(("set",))
            i += 1
            continue

        if action not in allowed:
            raise ValueError(
                f"Unknown action '{tokens[i]}' for {LIGHTING_MODES[mode][0]}.\n"
                f"Run 'python3 cli.py lighting {mode}' to see available actions."
            )

        if action == "speed":
            if i + 1 >= len(tokens):
                hint = "slow, medium, or fast"
                raise ValueError(f"speed requires a value ({hint}).")
            parsed.append(("speed", tokens[i + 1]))
            i += 2
        elif action == "brightness":
            if i + 1 >= len(tokens):
                raise ValueError("brightness requires a level (highest, high, medium, or low).")
            parsed.append(("brightness", tokens[i + 1]))
            i += 2
        elif action == "colour":
            i += 1
            index = None
            if caps["color_slots"] > 1:
                if i >= len(tokens):
                    raise ValueError(
                        f"colour requires a slot 1-{caps['color_slots']} and a colour."
                    )
                try:
                    index = int(tokens[i])
                except ValueError:
                    raise ValueError(
                        f"Colour slot must be a number 1-{caps['color_slots']}, then a colour."
                    )
                if index < 1 or index > caps["color_slots"]:
                    raise ValueError(
                        f"Invalid colour slot: {index}. Valid slots are 1-{caps['color_slots']}."
                    )
                i += 1
            rgb, consumed = parse_colour_tokens(tokens[i:])
            parsed.append(("colour", index, rgb))
            i += consumed
        else:
            raise ValueError(
                f"Unknown action '{tokens[i]}' for {LIGHTING_MODES[mode][0]}.\n"
                f"Run 'python3 cli.py lighting {mode}' to see available actions."
            )
    return parsed


def apply_mode_actions(mode: int, tokens) -> int:
    from main import apply_mode_settings

    parsed = parse_actions(mode, tokens)
    device = initialize(VENDOR_ID, PRODUCT_ID)
    settings = []
    messages = []
    for item in parsed:
        kind = item[0]
        if kind == "set":
            continue
        if kind == "speed":
            raw = str(item[1]).lower()
            if MODE_CAPABILITIES[mode]["speed"] == "trail":
                if raw not in TRAIL_SPEED:
                    raise ValueError(
                        f"Invalid trail speed: {item[1]}. Use slow, medium, or fast."
                    )
                value = TRAIL_SPEED[raw]
                settings.append(("speed", value))
                messages.append(f"✓ Speed set to: {TRAIL_SPEED_LABELS[value]}")
            else:
                if raw not in SPEED_65:
                    raise ValueError(
                        f"Invalid speed: {item[1]}. Use slow, medium, or fast."
                    )
                value = SPEED_65[raw]
                settings.append(("speed", value))
                messages.append(f"✓ Speed set to: {SPEED_65_LABELS[value]}")
        elif kind == "brightness":
            raw = str(item[1]).lower()
            if raw not in BRIGHTNESS_LEVELS:
                raise ValueError(
                    f"Invalid brightness: {item[1]}. Use highest, high, medium, or low."
                )
            value = BRIGHTNESS_LEVELS[raw]
            settings.append(("brightness", value))
            messages.append(f"✓ Brightness set to: {BRIGHTNESS_LABELS[value]}")
        elif kind == "colour":
            _kind, index, rgb = item
            r, g, b = rgb
            settings.append(("colour", index, rgb))
            slot = "" if MODE_CAPABILITIES[mode]["color_slots"] == 1 else f" {index}"
            extra = ""
            if mode == 6 and index == 5:
                extra = " (following 3 bytes copied from slot 5)"
            named = get_color_name(r, g, b)
            suffix = f" ({named})" if named else ""
            messages.append(f"✓ Colour{slot} set to: R={r} G={g} B={b}{suffix}{extra}")
    print("settings", settings)
    apply_mode_settings(device, mode, settings)
    print(f"✓ Lighting mode set to: {LIGHTING_MODES[mode][0]}")
    for message in messages:
        print(message)

    return 0


def handle_color(args):
    """
    Legacy colour handler kept for existing tests.
    """
    if hasattr(args, 'r') and args.r is not None:
        if args.g is None or args.b is None:
            display_color_usage()
            return 0
        set_lighting_color(args.r, args.g, args.b)
    else:
        display_color_usage()
    return 0


def display_color_usage():
    print("Usage: python3 cli.py lighting <mode> colour ...")
    print("Run 'python3 cli.py lighting <mode>' to see colour options for that mode.")
    print()
    display_common_colours()


def set_lighting_color(r: int, g: int, b: int):
    """
    Validates RGB range, initializes device, calls set_colour.
    """
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(
            f"Invalid RGB value. All RGB values must be 0-255.\n"
            "Run 'python3 cli.py lighting 2' for usage and examples."
        )

    from main import set_colour

    device = initialize(VENDOR_ID, PRODUCT_ID)
    set_colour(device, (r, g, b))

    color_name = get_color_name(r, g, b)
    if color_name:
        print(f"✓ Colour set to: R={r} G={g} B={b} ({color_name})")
    else:
        print(f"✓ Colour set to: R={r} G={g} B={b}")


def get_color_name(r: int, g: int, b: int) -> str | None:
    """
    Returns human-readable name for common colors.
    """
    return COMMON_COLORS.get((r, g, b))
