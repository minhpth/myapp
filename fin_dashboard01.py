# -*- coding: utf-8 -*-
###############################################################################
# FINANCIAL DASHBOARD #1 - v2.1
###############################################################################

#==============================================================================
# Initiating
#==============================================================================

import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st

#==============================================================================
# Main body
#==============================================================================

# --- Title ---

# Add dashboard title and description
st.title("My simple financial dashboard")
st.write("Data source: Yahoo Finance")

# --- Insert an image ---

image = Image.open('./img/stock_market.jpg')
st.image(image, caption='Stock market')

# --- Multiple choices box ---

# Get the list of stock tickers from S&P500
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

# Add multiple choices box
tickers = st.multiselect("Ticker(s)", ticker_list)

# --- Select date time ---

# Add select begin-end date
col1, col2 = st.columns(2)  # Create 2 columns
start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=30))
end_date = col2.date_input("End date", datetime.today().date())

# --- Add a button ---

get = st.button("Get data", key="get")

# --- Table to show data ---

# Add table to show stock data
# This function get the stock data and save it to cache to resuse
@st.cache
def GetStockData(tickers, start_date, end_date):
    global get
    # Loop through the selected tickers
    stock_price = pd.DataFrame()
    for tick in tickers:
        stock_df = yf.Ticker(tick).history(start=start_date, end=end_date)
        stock_df['Ticker'] = tick  # Add the column ticker name
        stock_price = pd.concat([stock_price, stock_df], axis=0)  # Comebine results
    return stock_price.loc[:, ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Check if there is/are selected ticker(s)
def ShowTable():
    global tickers
    global stock_price
    if len(tickers) > 0:
        st.write('Stock price data')
        stock_price = GetStockData(tickers, start_date, end_date)
        st.dataframe(stock_price)

# --- Line plot ---

# Add a line plot
def ShowLinePlot():
    global tickers
    global stock_price
    if len(tickers) > 0:
        st.write('Close price')
        fig, ax = plt.subplots(figsize=(15, 5))
        for tick in tickers:
            stock_df = stock_price[stock_price['Ticker'] == tick]
            ax.plot(stock_df['Close'], label=tick)
        ax.legend()
        st.pyplot(fig)
    
# --- Show the above table and plot when the button is clicked ---

if get:
    ShowTable()
    ShowLinePlot()
    
###############################################################################
# END
###############################################################################