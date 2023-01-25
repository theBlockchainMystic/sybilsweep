from flask import Flask, request, jsonify
import requests
import time
import pandas as pd
import json
import pickle
import numpy as np
from eth_abi import abi

app = Flask(__name__)
apikey = "" ##create etherscan api key

# load saved model Isolation Forest
with open('models/isolation_forest' , 'rb') as f:
    isf = pickle.load(f)

# load saved model Robust Covariance
with open('models/robust_cov' , 'rb') as f:
    cov = pickle.load(f)

## get_block num
def get_block(timestamp):
    r = requests.post(f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={apikey}")
    results=r.json()
    return results['result']


## Normal Transactions By Address
def feature_store(start_block_num,end_block_num,wallet_address):
    normal_trans = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock={start_block_num}&endblock={end_block_num}&page=1&offset=10&sort=asc&apikey={apikey}"
    r = requests.post(normal_trans)
    print(wallet_address,r)
    results=r.json()
    #print(results['result'])
    if len(results['result'])>0:
        try:
            l=pd.DataFrame(results['result'])
        except:
            l=None
    else:
        l=None
    
    return l

## checks if wallets is used only for voting
def vote_only(start_block_num,end_block_num,source_wallets):
    results=[]
    print("###### Obtaining Wallet meta-data ######")
    for i in source_wallets:
        r=feature_store(start_block_num,end_block_num,i)
        if r is None:
            pass
        else:
            results.append(r)
    if len(results)>0:
        #print(results)
        temp_df=pd.concat(results)
        #print(temp_df)
        vl=list(temp_df[temp_df['functionName'].str.contains('vote')]['functionName'].dropna().unique())
        temp_df['classes'] = 1
        temp_df['classes']=temp_df['classes'].where(temp_df['functionName'].isin(vl),0)
        s1=pd.concat([temp_df.groupby(['from'])['classes'].count(),temp_df.groupby(['from'])['classes'].sum()],axis=1)
        s1=s1.reset_index()
        s1.columns = ['from','total','vote']
        s1['percent_vote'] = s1['vote']*100/s1['total']
        return list(s1[s1['percent_vote']==100]['from'].unique())
    else:
        return []

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

@app.route('/sybil',methods=['POST'])
def pipe():
    inp_json = request.json
    df = pd.DataFrame.from_dict(inp_json)
    source_wallets=list(set(df.source_wallet.unique()))
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
    ## Wallet check
    start_epoch = int(df.created_at.min().value/1e9)
    end_epoch = int(df.created_at.max().value/1e9)
    print('start_epoch: ',start_epoch, 'end_epoch: ',end_epoch)
    start_block_num = get_block(start_epoch)
    end_block_num = get_block(end_epoch)
    votes_only = vote_only(start_block_num,end_block_num,source_wallets)
    df['sybil_account'] = 'True'
    df['sybil_account']=df['sybil_account'].where(df['source_wallet'].isin(votes_only),'False')
    return df.to_json()

if __name__ == '__main__':
    app.run(debug=True)