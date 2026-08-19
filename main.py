from config import settings
from data import SQLRepo
from model import GarchModel
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import create_engine

# FitIn class -- data validation for the entering data (request)
class FitIn(BaseModel):
    ticker: str
    use_new_data: bool
    n_observations: int
    p: int
    q: int

#FitOut class -- data validation for data coming back from the api (response)    
class FitOut(BaseModel):
    success: bool
    message: str   
    
# data validation for the in-data for the predict path    
class PredictIn(BaseModel):
    ticker: str
    n_days: int   

# data validation for the out-data from the predict path    
class PredictOut(BaseModel):
    success: bool
    forecast: dict
    message: str      

# helper function as every time we need to inistanciate the garch model and the model needs to connect to sqlserver database throug the repo object "as pre the model module"
# instead of making it as a path we will make it as a helper function
def build_model(ticker, use_new_data):
    
    engine = create_engine("mssql+pyodbc://sa:0121482088Om@localhost:1433/APIDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")
    repo = SQLRepo(connection=engine)
    model = GarchModel(ticker=ticker, use_new_data=use_new_data, repo=repo)
    return model





app = FastAPI()

@app.get("/hello", status_code=200)
def hello():
    return {"message": "Hello world"}


# i am telling the server to do something so it's not a get request it's a POST request
# eh el data model elli hresponse beh, response teqban lil fitout class
@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request:FitIn): # request here follows the attrs of the FitIn
    """Fit model, return comfirmation message

    Args:
        request:FitIn
        
    returns:
        dict, Must conform to FitOut class    
    """
    
    # create response dict from the request
    response = request.model_dump()
    
    try:
        
        # build model using build model function
        model = build_model(ticker=request.ticker, use_new_data=request.use_new_data)
        
        model.wrangle_data(n_observations=request.n_observations)
        
        model.fit(p=request.p, q=request.q)
        
        file_name = model.dump()
        
        response["success"] = True
        response["message"] = f"Trained and saved '{file_name}'"
        
    except Exception as e:
        response["success"] = False 
        response["message"] = str(e) 
    return response      


@app.post("/predict", status_code=200, response_model=PredictOut)
def predict(request:PredictIn):
    response=request.model_dump()
    
    try:
        model = build_model(ticker=request.ticker, use_new_data=False)
        model.load()
        predictions = model.predict_volatility(horizon=request.n_days)
        response["success"]=True
        response["forecast"]=predictions
        response["message"]="prediction done"
        
    except Exception as e:
        response["success"] = False
        response["forecast"] = {}
        response["message"] = str(e) 
    
    return response    