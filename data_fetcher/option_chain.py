import pandas as pd
import requests


class OptionChainFetcher:
    def __init__(self, symbol):
        self.symbol = symbol
        self.url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_option_chain(self):
        session = requests.Session()
        session.headers.update(self.headers)
        response = session.get(self.url)

        if response.status_code == 200:
            data = response.json()
            if "records" in data and "data" in data["records"]:
                option_data = data["records"]["data"]
                expiry_dates = data["records"]["expiryDates"]
                return option_data, expiry_dates
            else:
                print("Invalid response structure")
        else:
            print(f"Failed to retrieve data: {response.status_code}")
        return None, None


class OptionChainProcessor:
    def __init__(self, option_chain, selected_expiry_date):
        self.option_chain = option_chain
        self.selected_expiry_date = selected_expiry_date

    def create_option_chain_table(self):
        rows = []
        for option in self.option_chain:
            if option["expiryDate"] == self.selected_expiry_date:
                row = self._create_row(option)
                rows.append(row)
        return pd.DataFrame(rows)

    def _create_row(self, option):
        row = {
            "CALL OI": option["CE"]["openInterest"] if "CE" in option else None,
            "CALL CHNG IN OI": (
                option["CE"]["changeinOpenInterest"] if "CE" in option else None
            ),
            "CALL VOLUME": (
                option["CE"]["totalTradedVolume"] if "CE" in option else None
            ),
            "CALL IV": option["CE"]["impliedVolatility"] if "CE" in option else None,
            "CALL LTP": option["CE"]["lastPrice"] if "CE" in option else None,
            "CALL CHNG": option["CE"]["change"] if "CE" in option else None,
            "CALL BID QTY": option["CE"]["bidQty"] if "CE" in option else None,
            "CALL BID": option["CE"]["bidprice"] if "CE" in option else None,
            "CALL ASK": option["CE"]["askPrice"] if "CE" in option else None,
            "CALL ASK QTY": option["CE"]["askQty"] if "CE" in option else None,
            "STRIKE": option["strikePrice"],
            "PUT BID QTY": option["PE"]["bidQty"] if "PE" in option else None,
            "PUT BID": option["PE"]["bidprice"] if "PE" in option else None,
            "PUT ASK": option["PE"]["askPrice"] if "PE" in option else None,
            "PUT ASK QTY": option["PE"]["askQty"] if "PE" in option else None,
            "PUT CHNG": option["PE"]["change"] if "PE" in option else None,
            "PUT LTP": option["PE"]["lastPrice"] if "PE" in option else None,
            "PUT IV": option["PE"]["impliedVolatility"] if "PE" in option else None,
            "PUT VOLUME": option["PE"]["totalTradedVolume"] if "PE" in option else None,
            "PUT CHNG IN OI": (
                option["PE"]["changeinOpenInterest"] if "PE" in option else None
            ),
            "PUT OI": option["PE"]["openInterest"] if "PE" in option else None,
        }
        return row
