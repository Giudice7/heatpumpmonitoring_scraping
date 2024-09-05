import pandas as pd


def create_dataframe_from_feed_data(feed_data):
    """
    Convert a list of dictionaries with 'feedid' and 'data' keys into a pandas DataFrame.

    :param feed_data: List of dictionaries where each dictionary contains 'feedid' and 'data'.

    :return: A pandas DataFrame with 'feedid' as column names and their corresponding 'data' as column values.
    """
    # Initialize an empty dictionary to store data for the DataFrame
    data_dict = {}

    # Loop through the list of feed data dictionaries
    for feed in feed_data:
        feedid = feed['feedid']
        data = feed['data']

        # Assign the data to the feedid in the dictionary
        data_dict[feedid] = data

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(data_dict)

    return df


if __name__ == "__main__":
    # Example usage
    feed_data = [
        {"feedid": 499959, "data": [1, 2, 3, 4]},
        {"feedid": 499960, "data": [5, 6, 7, 8]},
        {"feedid": 499973, "data": [9, 10, 11, 12]},
    ]

    df = create_dataframe_from_feed_data(feed_data)
    print(df)
