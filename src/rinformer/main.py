import os

from .model import Weather

def main():

    # weather_api = os.getenv("WORLD_AIR_QUALITY_API_TOKEN")
    # if weather_api is None:
    #     raise ValueError
    # weather = Weather(token=weather_api)
    weather = Weather()
    data = weather.query()
    print("\t\N{Hot Beverage}" + f"{data}")

if __name__ == "__main__":
    main()