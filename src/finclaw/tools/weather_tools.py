from ..weather.weatherapi import weatherapi


def register_weather_tools(mcp) -> None:
    @mcp.tool()
    def weather_forcast(city: str, days: int) -> str:
        """Weather forcast

        Args:
            city: Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name
            days: Number of days of weather forecast. Value ranges from 1 to 14
        """
        data = weatherapi.shoot(city, days)
        return data