# Please `pip install transformers accelerate`
from transformers import pipeline


pipeline = pipeline(
    "text-generation",
    model="Nexusflow/NexusRaven-V2-13B",
    torch_dtype="auto",
    device_map="auto",
)

prompt_template = \
'''
Function:
def get_weather_data(coordinates):
    """
    Fetches weather data from the Open-Meteo API for the given latitude and longitude.

    Args:
    coordinates (tuple): The latitude of the location.

    Returns:
    float: The current temperature in the coordinates you've asked for
    """

Function:
def get_coordinates_from_city(city_name):
    """
    Fetches the latitude and longitude of a given city name using the Maps.co Geocoding API.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: The latitude and longitude of the city.
    """

User Query: {query}<human_end>

'''

prompt = prompt_template.format(query="What's the weather like in Seattle right now?")

result = pipeline(prompt, max_new_tokens=2048, return_full_text=False, do_sample=False, temperature=0.001)[0]["generated_text"]
print (result)
