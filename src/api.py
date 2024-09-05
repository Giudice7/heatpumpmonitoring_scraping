import requests


def fetch_emoncms_data(start, end, interval=60, average=1, delta=0, skipmissing=0, limitinterval=0,
                       timeformat="notime", app_url=None, ids=None):
    # Build the base URL
    url = "https://emoncms.org/feed/data.json"
    # Convert ids list to a comma-separated string
    ids_param = ",".join(map(str, ids)) if ids else ""

    # Build the query parameters
    params = {
        "start": start,
        "end": end,
        "interval": interval,
        "average": average,
        "delta": delta,
        "skipmissing": skipmissing,
        "limitinterval": limitinterval,
        "timeformat": timeformat,
        "ids": ids_param,
        "apikey": app_url.split('readkey=')[1]
    }

    # Headers
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'EMONCMS_SESSID=gtml66d05j9krvq2rebopgqrks',
        'Referer': app_url,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    # Make the request
    response = requests.get(url, headers=headers, params=params)

    # Return the response data
    return response.json()


def fetch_feed_list(app_url):
    """
    Fetch the list of feeds from the EmonCMS API and return it as a pandas DataFrame.

    :param app_url: The URL of the EmonCMS application.
    :return: A json containing the list of feeds.
    """
    url = "https://emoncms.org/feed/list.json"

    # Headers (Static in this case)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'EMONCMS_SESSID=gtml66d05j9krvq2rebopgqrks',
        'Referer': app_url,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    # Set up the query parameters with the API key
    params = {
        'apikey': app_url.split('readkey=')[1]
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    # Parse the JSON response
    feed_list = response.json()

    return feed_list


def fetch_ids():
    """
    Fetch the list of ids from the EmonCMS API and return it.
    :return: dictionary with ids and other info
    """
    url = "https://heatpumpmonitor.org/system/stats/last90"

    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'HPMON_ORG_SESSID=q61929n841livfe57r3qb0qic3',
        'priority': 'u=1, i',
        'referer': 'https://heatpumpmonitor.org/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
