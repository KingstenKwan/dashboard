#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime


# In[2]:


url = 'https://raw.githubusercontent.com/KingstenKwan/Crypto_dataset/main/'
csv_files = [
    "coin_Aave.csv", "coin_BinanceCoin.csv", "coin_Bitcoin.csv", 
    "coin_Cardano.csv", "coin_ChainLink.csv", "coin_Cosmos.csv", 
    "coin_CryptocomCoin.csv", "coin_Dogecoin.csv", "coin_EOS.csv",
    "coin_Ethereum.csv", "coin_Iota.csv", "coin_Litecoin.csv", 
    "coin_Monero.csv", "coin_NEM.csv", "coin_Polkadot.csv", 
    "coin_Solana.csv", "coin_Stellar.csv", "coin_Tether.csv", 
    "coin_Tron.csv", "coin_Uniswap.csv", "coin_USDCoin.csv", 
    "coin_WrappedBitcoin.csv", "coin_XRP.csv"
]

df_list = []
for file in csv_files: 
    df = pd.read_csv(url + file)
    df_list.append(df)


# In[7]:


app = dash.Dash(__name__)

server = app.server

dropdown_options = [{"label": crypto[5:-4], "value": crypto[5:-4]} for crypto in csv_files]

app.layout = html.Div([
    html.H1(children = "Cryptocurrency Dashboard",
           style = {
               'textAlign':'center',
           }),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label="Pricing History", children=[
            html.Div([
                html.Div(id="filter-options", children=[
                    html.Button("Daily", id="btn-daily", n_clicks=0),
                    html.Button("Quarterly", id="btn-quarterly", n_clicks=0),
                    html.Button("Yearly", id="btn-yearly", n_clicks=0),
                    dcc.Graph(id="price-graph"),
                ]),
            ])
        ]),
        dcc.Tab(label="My Portfolio", children=[
            html.Div([
                html.H3("New Transaction"),
                
                html.Label("Cryptocurrency Code: "),
                dcc.Dropdown(
                    id="input-code",
                    options=dropdown_options,
                    value="Aave"
                    ),
                html.Br(),
                html.Br(),
                
                html.Label("Date of Transaction: "),
                dcc.DatePickerSingle(
                    id="input-date",
                    date=datetime.now().date(),
                    display_format="YYYY-MM-DD",
                    placeholder="Select a date",
                    style={"margin-bottom": "20px"}
                    ),
                html.Br(),
                
                html.Label("Buy/Sell: "),
                dcc.Dropdown(
                    id="input-buy-sell",
                    options=[
                        {"label": "Buy", "value": "Buy"},
                        {"label": "Sell", "value": "Sell"}
                    ],
                    value="Buy"
                ),
                html.Br(),
                html.Br(),
                
                html.Label("Amount in Cryptocurrency Units: "),
                dcc.Input(id="input-amount", type="number"),
                html.Br(),
                html.Br(),
                
                html.Button("Add Transaction", id="btn-add-transaction", n_clicks=0),
                html.Div(id="transaction-feedback")
            ])
        ]),
    ]),
])


# In[8]:


@app.callback(
    Output("price-graph", "figure"),
    Input("btn-daily", "n_clicks"),
    Input("btn-quarterly", "n_clicks"),
    Input("btn-yearly", "n_clicks"),
)

def update_graph(n_daily, n_quarterly, n_yearly):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "btn-daily" in changed_id:
        interval = "D"
    elif "btn-quarterly" in changed_id:
        interval = "Q"
    elif "btn-yearly" in changed_id:
        interval = "Y"
    else:
        interval = "D"
        
    crypto_data = pd.concat(df_list)
    crypto_data = crypto_data[['Name','Date','Close']]
    crypto_data["x axis"] = crypto_data["Date"]
    crypto_data["Date"] = pd.to_datetime(crypto_data["Date"])
    df_resampled = crypto_data.groupby([pd.Grouper(key='Date', freq=interval), 'Name'])['Close'].mean().reset_index()
    fig = px.line(df_resampled, x='Date', y='Close', color='Name', title = "History Price of Cryptocurrency")
    
    fig.update_layout(xaxis_tickformat='%Y-Q%q')

    return fig


# In[9]:


@app.callback(
    Output("transaction-feedback", "children"),
    Input("btn-add-transaction", "n_clicks"),
    State("input-code", "value"),
    State("input-date", "date"),
    State("input-buy-sell", "value"),
    State("input-amount", "value"),
)

def add_transaction(n_clicks, code, date, buy_sell, amount):
    if n_clicks > 0:
        print(f"New Transaction: Code - {code}, Date - {date}, Buy/Sell - {buy_sell}, Amount -{amount}")
        return "Transaction added successfully!"      
    return ""


# In[12]:


app.run(jupyter_mode="external")
import os
os.environ['PORT'] = '8080'

