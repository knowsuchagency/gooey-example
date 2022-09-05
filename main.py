from argparse import ArgumentParser

import httpx
from geocode.geocode import Geocode
from gooey import Gooey


@Gooey(program_name="Demo Weather App")
def main():
    gc = Geocode()
    gc.load()

    parser = ArgumentParser(description="Get weather forecast")

    parser.add_argument(
        "city",
        metavar="City",
        help="Enter the name of a city",
        default="Los Angeles, CA",
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
