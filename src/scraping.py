import requests
from bs4 import BeautifulSoup
import re


def get_app_url(id_hp: int):
    """
    Scrapes the API key from the heat pump monitor website.
    :param id_hp: the id of the heat pump
    :return: the api key
    """
    # URL of the page to scrape
    url = f"https://heatpumpmonitor.org/system/view?id={id_hp}"

    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Convert the soup to string and search for the key using regex
    html_str = str(soup)
    match = re.search(r'"url":"(.*?)",', html_str)
    if match:
        app_url = match.group(1)
        # Delete the quotes, double queotes and '\' characters
        app_url = app_url.replace('"', '')
        app_url = app_url.replace('\\', '')
        app_url = app_url.replace(' ', '')
        return app_url
    else:
        return None
