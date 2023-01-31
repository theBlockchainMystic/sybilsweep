from flask import Flask, request, jsonify
import requests
import time
import pandas as pd
import json
import pickle
import numpy as np

app = Flask(__name__)

# load saved model Isolation Forest
with open('models/isolation_forest' , 'rb') as f:
    isf = pickle.load(f)

# load saved model Robust Covariance
with open('models/robust_cov' , 'rb') as f:
    cov = pickle.load(f)


def ss(df):
    if df['amount'].std()>0:
        df['ss_amount']=(df['amount']-df['amount'].mean())/df['amount'].std()
    else:
        df['ss_amount']=df['amount']-df['amount'].mean()
    return df

def prepocess(data):
    data.created_at = pd.to_datetime(data.created_at)
    data=data.sort_values('created_at').reset_index()
    data=data.drop(columns='index')
    data=data.groupby(['token']).apply(ss)
    _df1=data.groupby(['destination_wallet','token']).apply(lambda x:x['created_at'].diff()).reset_index()
    _df1=_df1.sort_values('level_2')
    data["time_diff"]=_df1['created_at']
    data["time_diff"] = data["time_diff"].fillna(pd.Timedelta(seconds=0))
    data["time_diff"]=data["time_diff"].astype('timedelta64[s]')
    data=data.reset_index()
    data=data.drop(columns='index')
    return data

@app.route('/sybilsweep',methods=['POST'])
def pipe():
    inp_json = request.json
    df = pd.DataFrame.from_dict(inp_json)
    ## Prediction
    df = prepocess(df)
    X = df[['ss_amount','time_diff']].values
    df['isolation_forest_score']=isf.score_samples(X)
    df['robust_cov_score']=cov.mahalanobis(X)
    df['isolation_forest_prediction']=isf.predict(X)
    df['isolation_forest_prediction']=df['isolation_forest_prediction'].map({-1: 'True', 1: 'False'})
    df['robust_cov_prediction']=cov.predict(X)
    df['robust_cov_prediction']=df['robust_cov_prediction'].map({-1: 'True', 1: 'False'})
    df=df[['id', 'token', 'amount', 'source_wallet', 'destination_wallet','created_at', 'isolation_forest_prediction','isolation_forest_score','robust_cov_prediction','robust_cov_score']]
    return df.to_json()

if __name__ == '__main__':
    app.run(debug=True)