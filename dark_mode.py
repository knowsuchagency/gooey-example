import platform
import subprocess as sp


def macos_darkmode_enabled() -> bool:
    if platform.uname().system == "Darwin":
        cmd = "defaults read -g AppleInterfaceStyle"
        color_mode = sp.run(
            cmd.split(),
            capture_output=True,
            universal_newlines=True,
        ).stdout.strip()
        if color_mode == "Dark":
            return True
    return False


MACOS_DARK_MODE_ENABLED = macos_darkmode_enabled()


GLOBAL_DARK_MODE_DEFAULTS = (
    {
        "body_bg_color": "#262626",
        "header_bg_color": "#262626",
        "footer_bg_color": "#262626",
        "sidebar_bg_color": "#262626",
        "terminal_font_color": "#ffffff",
    }
    if MACOS_DARK_MODE_ENABLED
    else {}
)

ITEM_DARK_MODE_DEFAULTS = (
    {
        "error_color": "#ea7878",
        "label_color": "#ffffff",
        "help_color": "#8a7f7f",
    }
    if MACOS_DARK_MODE_ENABLED
    else {}
)
