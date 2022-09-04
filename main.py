import platform
import subprocess as sp

import httpx
from geocode.geocode import Geocode
from gooey import Gooey, GooeyParser


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


@Gooey(
    program_name="Demo Weather App",
    **GLOBAL_DARK_MODE_DEFAULTS,
)
def main():
    gc = Geocode()
    gc.load()

    parser = GooeyParser(description="Get weather forecast")

    if MACOS_DARK_MODE_ENABLED:
        for group in parser.parser._action_groups:
            group.gooey_options = {
                "label_color": "#ffffff",
                "description_color": "#363636",
            }

    parser.add_argument(
        "city",
        metavar="City",
        help="Enter the name of a city",
        default="Los Angeles, CA",
        gooey_options=ITEM_DARK_MODE_DEFAULTS,
    )

    args = parser.parse_args()

    city = args.city

    geocode = gc.decode(city)[0]

    latitude, longitude = geocode["latitude"], geocode["longitude"]

    grid_resp = httpx.get(
        f"https://api.weather.gov/points/{latitude:.4f},{longitude:.4f}"
    )

    grid_resp_json = grid_resp.json()

    props = grid_resp_json["properties"]

    grid_x, grid_y, office = (
        props["gridX"],
        props["gridY"],
        props["cwa"],
    )

    forecast_resp = httpx.get(
        f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
    )

    forecast_data = forecast_resp.json()

    for period in forecast_data["properties"]["periods"][:3]:

        name, forecast, temp, temp_unit, wind_dir, wind_spd = (
            period["name"],
            period["shortForecast"],
            period["temperature"],
            period["temperatureUnit"],
            period["windDirection"],
            period["windSpeed"],
        )

        print(
            f"{city} {name}: {forecast} with a temperature of {temp}{temp_unit} and winds {wind_spd} {wind_dir}"
        )

        print("-" * 80)


if __name__ == "__main__":
    main()
