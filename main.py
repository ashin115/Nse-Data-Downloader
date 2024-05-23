import logging
import time

import config
from data_fetcher.option_chain import OptionChainFetcher, OptionChainProcessor
from utils import save_to_csv


def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value}): ").strip()
    return user_input if user_input else default_value


def fetch_latest_expiry_date(fetcher, retries=3):
    for attempt in range(retries):
        try:
            option_chain, expiry_dates = fetcher.get_option_chain()
            if expiry_dates:
                return expiry_dates[0]  # Assuming the first expiry date is the latest
            else:
                logging.warning("No expiry dates found. Retrying...")
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait a bit before retrying
    raise ValueError("Failed to fetch expiry dates after several attempts.")


def display_option_chain(symbol, expiry_date, refresh_interval):
    fetcher = OptionChainFetcher(symbol)

    while True:
        try:
            option_chain, expiry_dates = fetcher.get_option_chain()

            if option_chain:
                processor = OptionChainProcessor(option_chain, expiry_date)
                df = processor.create_option_chain_table()

                if not df.empty:
                    save_to_csv(df)
                    logging.info("===== Option Chain Updated =====")
                    logging.info(f"Data saved to CSV at {time.ctime()}")
                else:
                    logging.warning("No data found for the selected expiry date")
            else:
                logging.warning("No option chain data found")

            time.sleep(refresh_interval)

        except KeyboardInterrupt:
            logging.info("Process interrupted by user. Exiting...")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(refresh_interval)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Market Data Viewer")

    symbol = get_user_input("Enter the symbol", config.SYMBOL)
    refresh_interval = get_user_input(
        "Enter the refresh interval (seconds)", str(config.REFRESH_INTERVAL)
    )

    try:
        refresh_interval = int(refresh_interval)
    except ValueError:
        logging.error("Invalid refresh interval. Using default value.")
        refresh_interval = config.REFRESH_INTERVAL

    fetcher = OptionChainFetcher(symbol)

    try:
        latest_expiry_date = fetch_latest_expiry_date(fetcher)
        expiry_date = get_user_input("Enter the expiry date", latest_expiry_date)
    except ValueError as e:
        logging.error(e)
        return

    display_option_chain(symbol, expiry_date, refresh_interval)


if __name__ == "__main__":
    main()
