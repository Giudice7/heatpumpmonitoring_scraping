if __name__ == "__main__":
    from scraping import get_app_url
    from fetch import fetch_data
    from api import fetch_ids

    id_list = fetch_ids()

    id_hp_list = [id_hp for id_hp in id_list]

    for id_hp in id_hp_list:
        start = "2024-01-01 00:00:00"
        end = "2024-08-31 23:59:59"
        try:
            app_url = get_app_url(id_hp=id_hp)
            if 'readkey' in app_url:
                data = fetch_data(id_hp=id_hp, app_url=app_url, start=start, end=end)
            else:
                print(f"No readkey found in app_url for id_hp {id_hp}")
        except Exception as e:
            print(f"Error fetching data for id_hp {id_hp}: {e}")