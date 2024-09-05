import os
import json
import pytz
import datetime
import pandas as pd
from utils import create_dataframe_from_feed_data
from api import fetch_emoncms_data, fetch_feed_list


def fetch_data(id_hp: int, app_url: str, start: str, end: str):
    """
    Fetch data from the EmonCMS API for a specific heat pump system.
    :param id_hp: id of the heat pump
    :param app_url: URL of the EmonCMS application
    :param start: start date in format "YYYY-MM-DD HH:MM:SS"
    :param end: end date in format "YYYY-MM-DD HH:MM:SS"
    :return:
    """

    rome_tz = pytz.timezone('Europe/Rome')

    # Set your start and end dates directly in the Europe/Rome timezone
    start_date = rome_tz.localize(datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S"))
    end_date = rome_tz.localize(datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))

    # Calculate the offest from UTC
    utc_offset_start = start_date.utcoffset().total_seconds()
    utc_offset_end = end_date.utcoffset().total_seconds()
    # Add the offset to the start and end dates
    start_date = start_date + datetime.timedelta(seconds=utc_offset_start)
    end_date = end_date + datetime.timedelta(seconds=utc_offset_end)

    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    timestamps = list(range(start_timestamp, end_timestamp, 60 * 1000))

    # Divide into groups of max 50000 elements to avoid memory errors during queries
    n = 50000
    timestamp_groups = [timestamps[i:i + n] for i in range(0, len(timestamps), n)]

    feed_list = fetch_feed_list(app_url=app_url)
    feed_info = {feed['id']: feed['name'] for feed in feed_list}
    list_ids = list(feed_info.keys())
    list_ids = [int(var_id) for var_id in list_ids]

    # Divide the list_ids in group of maximum five elements to avoid memory errors
    n = 5
    list_ids = [list_ids[i:i + n] for i in range(0, len(list_ids), n)]

    df_list = []
    for ts_group in timestamp_groups:
        df_ts_group = pd.DataFrame()
        for ids_group in list_ids:
            data = fetch_emoncms_data(start=ts_group[0],
                                      end=ts_group[-1],
                                      app_url=app_url,
                                      ids=ids_group)
            df = create_dataframe_from_feed_data(data)
            df_ts_group = pd.concat([df_ts_group, df], axis=1)
        df_ts_group['timestamp'] = ts_group
        df_list.append(df_ts_group)

    # Concatenate the DataFrames
    result_df = pd.concat(df_list, ignore_index=True)
    result_df = result_df.set_index('timestamp').sort_index()

    feed_info = {key: value for key, value in feed_info.items() if key in result_df.columns}

    # Reformat dataframe
    result_df = result_df.rename(columns=feed_info)
    result_df.reset_index(inplace=True)
    result_df['timestamp'] = pd.to_datetime(result_df['timestamp'], unit='ms')

    if not os.path.exists('../data'):
        os.makedirs('../data')

    result_df.to_csv(f'../data/{id_hp}.csv', index=False)
    with open(f'../data/{id_hp}.json', 'w') as f:
        json.dump(feed_list, f)

    return {
        "metadata": feed_list,
        "data": result_df
    }
