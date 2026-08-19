import os
from glob import glob
import joblib
import pandas as pd
from arch import arch_model
from config import settings
from data import AlphaVantageAPI, SQLRepo

class GarchModel:
    """Class for training Garch model and genereating prediction
    Attributes:
    -----------
    ticker: str
        Ticker symbol of stock whose volatility will be predicted
    repo: SQLRepo
        the repository where the data will be stored
    use_new_data: bool
        whether to get the new data of the ticker from alphavantage api 
        or use the excisted data in out sql database
    model_directory: str
        path of the directory where the model will be stored
        
    Methods:
    --------
    wrangle_data:
        generate stock returns from data in database
    fit:
        fit model to the training data
    predict:
        generate volatility forecast from the trained model
    dump:
        save trained model to file
    load:
        load trained model from file                               
    """
    
    def __init__(self, ticker: str, repo: SQLRepo, use_new_data: bool = False):
        self.ticker = ticker
        self.repo = repo
        self.use_new_data = use_new_data
        self.model_directory = settings.model_directory
        
    def wrangle_data(self, n_observations):
        """Extract data from database or (from alphavantage api)
        n_observations: int
            number of observatios to retrieve from database
        returns: None     
        """
        # get data from alphavantage api
        if self.use_new_data:
            av = AlphaVantageAPI()
            new_data = av.get_daily(ticker=self.ticker)
            self.repo.insert_table(data_frame=new_data, table_name=self.ticker)
            
        # get data from out database
        df = self.repo.read_sql(table_name=self.ticker)
        
        # clean data, attach it to the class as a "data" instance attribute
        df.sort_index(ascending=True, inplace=True)
        df["return"] = df["close"].pct_change()*100
        self.data=df["return"].dropna()
        
    def fit(self, p:int, q:int):
        """Create model, fit the model to self.data, attach model to self.model as instance attribute
                Parameters
                ----------
                p : int
                    Lag order of the symmetric innovation

                q : ind
                    Lag order of lagged volatility

                Returns
                -------
                None
                """
        self.model = arch_model(self.data,p=p, q=q, rescale=False).fit(disp=0)
        
    def __clean_prediction(self, predictions):
        """Reformat model prediction to json
        
        parameters: 
            prediction: pd.DataFrame [variance from ARCHMODEL forecast]
        Returns:
            Forecast of volatility: each key is a date in iso 8601 format,
            each value is predicted volatiolity """
        
        start = predictions.index[0] + pd.DateOffset(days=1)
        predictions_dates = pd.bdate_range(start=start, periods=predictions.shape[1])
        predictions_index = [d.isoformat() for d in predictions_dates]  
        data = predictions.values.flatten()**0.5
        predictions_formatted = pd.Series(data, index=predictions_index)
        return predictions_formatted.to_dict()
    
    
    def predict_volatility(self, horizon=5):
        """predicts volatility uysing self.model
        parameters:
            Horizon of forecase(for how many days): int 
            by defult 5
        returns: dict
            Forecast of volatility: each key is a date in iso 8601 format,
            each value is predicted volatiolity   
        """
        predictions = self.model.forecast(horizon=horizon, reindex=False).variance
        prediction_formatted = self.__clean_prediction(predictions)   
        return prediction_formatted  
         
         
    def dump(self):
        """save model to self.model_directory with time stamp
        returns:
            filepath:str where model was saved
        """
        timestamp = pd.Timestamp.now().isoformat()
        filepath = os.path.join(self.model_directory, f"{timestamp}_{self.ticker}.pkl")
        joblib.dump(self.model, filepath)
        
        return filepath
    
    def load(self):
        """load most recent model in self.model_directory for self.ticker
        attach model to self.model attribute
        """
        
        #  # Create pattern for glob search
        pattern = os.path.join(self.model_directory,f"*{self.ticker}.pkl")
        
        try:
            model_path = sorted(glob(pattern))[-1]
        except IndexError:
            raise Exception(f"No model trained for {self.ticker}")
        self.model = joblib.load(model_path)    
            
        
        
            
            
        