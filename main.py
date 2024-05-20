import time
import streamlit as st

from data_fetcher.option_chain import OptionChainFetcher, OptionChainProcessor
from utils import save_to_csv


def main():
    st.title("Option Chain Viewer")
    
    SYMBOL = st.text_input("Enter Symbol", "NIFTY")
    EXPIRY_DATE = st.text_input("Enter Expiry Date (dd-mmm-yyyy)", "23-May-2024")
    REFRESH_INTERVAL = st.number_input("Refresh Interval (seconds)", min_value=1, max_value=3600, value=5)

    fetcher = OptionChainFetcher(SYMBOL)

    if st.button("Fetch Data"):
        placeholder = st.empty()
        while True:
            option_chain, expiry_dates = fetcher.get_option_chain()
            
            if expiry_dates:
                selected_expiry_date = EXPIRY_DATE  # Use the user-defined expiry date

                if option_chain:
                    processor = OptionChainProcessor(option_chain, selected_expiry_date)
                    df = processor.create_option_chain_table()

                    if not df.empty:
                        save_to_csv(df)
                        placeholder.write(f"Data saved to CSV at {time.ctime()}")
                        placeholder.dataframe(df)
                    else:
                        placeholder.write("No data found for the selected expiry date")
                else:
                    placeholder.write("No option chain data found")
            else:
                placeholder.write("No expiry dates found for the symbol")

            time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()
