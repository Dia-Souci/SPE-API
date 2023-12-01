from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
app = FastAPI()

class ScoringItem(BaseModel):
    Budget : float
    FindingSource : float
    Category : str
    TRL_Start : int
    TRL_End : int

def CategoryHandler(e) :
    possibilities = ['Full Chain','T&S','capture','utilization']
    for _,pos in enumerate(possibilities) : 
        if e == pos :
            print(_)
            return _


with open("model.pkl",'rb') as f : 
    model = pickle.load(f)


@app. post('/')
async def scoring_endpoint(item:ScoringItem):
    data = item.dict()
    data['Category']=CategoryHandler(data['Category'])
    df= pd.DataFrame([data.values()] , columns= data.keys())
    yhat = model.predict(df)

    return { "prediction" : int(yhat)}
