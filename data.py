"""This is for all the code used to interact with the AlphaVantage API
and the SQLite database. Remember that the API relies on a key that is
stored in your `.env` file and imported via the `config` module.
"""

from config import Settings
import pandas as pd
import requests

settings = Settings()

class AlphaVantageAPI:
    def __init__(self, api_key = settings.alpha_vantage_api_key, base_url = "https://www.alphavantage.co"):
        self.alpha_vantage_api_key = api_key
        self.base_url = base_url
        
    
    def get_daily(self, ticker):
        """
        Get daily time series of a specific stock from Alphavantage api
        
        parameters:
            ticker: str
            the ticker symbol
            
        returns:
            pd.DataFrame 
                Columns are 'open', 'high', 'low', 'close', and 'volume'.
                All are numeric.    
        """
        
        # Build our ENDPOINT
        url = (
        f"{self.base_url}/query?"
        "function=TIME_SERIES_DAILY&"
        f"symbol={ticker}.BSE&"
        f"apikey={self.alpha_vantage_api_key}"
            )
        

        
        response = requests.get(url=url)
        response_data = response.json()
        
        # Defensive programming
        if "Time Series (Daily)" not in response_data.keys():
            raise Exception(f"Invalid API call, check that ticker symbol {ticker}")      
        stock_data = response_data["Time Series (Daily)"]  
        df= pd.DataFrame.from_dict(stock_data, orient="index", dtype="float")
        df.columns = [x[1] for x in df.columns.map(str.split)]
        df.index = pd.to_datetime(df.index)
        df.index.name="date"
        
        return df


class SQLRepo:

    def __init__(self, connection):
        self.connection = connection
        
    def insert_table(self,data_frame, table_name, if_exists = "replace"): 
        """ insert DataFrame into mssql database as a table
        Parameters: 
            table_name: str
            data_frame : pd.DataFrame
            table_name : str
            if_exists: str
                how to behave if the table already exists in the database
                - fail --> raise a ValueError
                - replace -->  drop the table before inserting new values
                - append --> insert new values to an existing table
        """  
        
        n_inserted = data_frame.to_sql(con = self.connection, name = table_name, if_exists = if_exists)
        
        return {
            "transaction_sccessful" : True,
            "observations_inserted" : n_inserted
        }
        
        
    def read_sql(self, table_name):
        """ Read table from mssql Database
        Parameters :
            table_name: str
            
        returns:
            pd.DataFrame   
                index: datetime index "date"
                columns: [open, high, low, close, volume]--> float 
        
        """    
        
        query = f"select * from {table_name}"
        df = pd.read_sql(query, con=self.connection, parse_dates=["date"], index_col="date")
        return df