from datetime import date, datetime 
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import locale
locale.setlocale( locale.LC_ALL, '' )

st.write("""
# Stock Market Portfolio Simulation

### A lesson on Ergodicity
""")

np.random.seed(9)
stocks_list = ['TSLA', 'XOM', 'GOOGL', 'SHOP', 'AAL', 'NDX', 'DJI']

@st.cache
def load_data(stocks_list):
    with st.spinner('Downloading ticker data ...'):
        stocks_price_df = yf.download(stocks_list, 
                        start='2000-01-01', 
                        end='2020-05-22', 
                        actions=True,
                        rounding=True,
                        progress=False)

    return stocks_price_df


def run_experiment(initial_amount, leverage, stock_analyze_pc_df):

    evt_data = {}
    gain_data = {}

    p_N = len(stocks_list)

    # generate data for every person
    for tick in stock_analyze_pc_df.columns:
        # start with initial amount as leverage
        person_gain = initial_amount
        
        # generate random events of gain / loss for N time steps
        evts = stock_analyze_pc_df[tick].iloc[1:].values.tolist()
        
        # temp state store for interim gains. Initialize it with the starting amount
        gains = [person_gain]
        
        # calc gain progression
        for e in evts:
            # st.write(e)
            person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 + e))
            gains.append(person_gain)

            
        gain_data[tick] = gains

    return gain_data


def plot_avgs(stock_gain_df, tickers):

    stock_gain_df = stock_gain_df.set_index("date")
    stock_gain_df = stock_gain_df.loc[:, tickers]

    fig = go.Figure()
    for t in tickers:
        fig.add_trace(go.Scatter(x=stock_gain_df.index, y=stock_gain_df[t], mode="lines", name=t))
    st.plotly_chart(fig, use_container_width=True)



def main():
    df = load_data(stocks_list)

    sl_initial_amount = 10000
    st.sidebar.markdown("### Set parameters for simulation")
    sl_leverage = st.sidebar.slider('Leverage', 0.0, 1.0, 1.0)
    sl_start_dt = st.sidebar.date_input('Choose investment start date', date(2016,1,10), date(2016,1,10))
    sl_end_dt = st.sidebar.date_input('Choose investment end date', date(2020, 1, 31), date(2016,1,10))
    sl_select_tickers = st.sidebar.multiselect("Selet tickers to compare performance",
                            stocks_list,
                            stocks_list)

    df_slice = df.loc[(df.index >= np.datetime64(sl_start_dt)) & (df.index <= np.datetime64(sl_end_dt))]

    st.write(f"""
    ### Parameters

    * Initial Amount = {locale.currency(sl_initial_amount, grouping=True)}
    * Leverage = {sl_leverage}
    * Investment Start Date = {sl_start_dt}
    * Investment End Date = {sl_end_dt}
    """)

    # cleanup data for adjusted change values
    stock_analyze_df = df_slice.iloc[:,:7].copy()
    stock_analyze_df.columns = stock_analyze_df.columns.droplevel()
    stock_analyze_df = stock_analyze_df.fillna(method="ffill", inplace=False)

    # calc change percentage
    stock_analyze_pc_df = stock_analyze_df.apply(lambda x: (x - x.shift(1))/x.shift(1))
    stock_analyze_pc_df = stock_analyze_pc_df.fillna(0)


    # run simulation on button press
    if st.sidebar.button("Run Simulation", "run-exp-btn"):
        if sl_end_dt > sl_start_dt:
            gain_data = run_experiment(sl_initial_amount, sl_leverage, stock_analyze_pc_df)
            stock_gain_df = pd.DataFrame(gain_data)
            stock_gain_df["date"] = stock_analyze_pc_df.index

            plot_avgs(stock_gain_df, sl_select_tickers)
        else:
            st.sidebar.error("Enter valid dates")



if __name__ == "__main__":
    main()
