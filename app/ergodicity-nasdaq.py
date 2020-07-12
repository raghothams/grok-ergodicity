from datetime import date, datetime, timedelta
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import locale
locale.setlocale(locale.LC_ALL, '')

st.write("""
# Stock Market Portfolio Simulation

### A lesson on Ergodicity with stock market
""")

np.random.seed(9)
equity_list = pd.read_csv("data/equity_list.csv")

start_date_year = 2004
start_date_month = 1
start_date_day = 10

start_date = str(start_date_year) + "-" + \
    str(start_date_month) + "-" + str(start_date_day)
end_date = date.today() - timedelta(days=1)


@st.cache
def load_data(equity_list):
    with st.spinner('Downloading ticker data ...'):
        stocks_price_df = yf.download(equity_list.Ticker.tolist(),
                                      start=start_date,
                                      end=end_date.strftime("%Y-%m-%d"),
                                      actions=True,
                                      rounding=True,
                                      progress=False)

    return stocks_price_df


def run_experiment(initial_amount, leverage, stock_analyze_pc_df):

    evt_data = {}
    gain_data = {}

    p_N = len(equity_list)

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
            person_gain = (person_gain * (1 - leverage)) + \
                (person_gain * leverage * (1 + e))
            gains.append(person_gain)

        gain_data[tick] = gains

    return gain_data


def plot_avgs(stock_gain_df, equity_name):

    stock_gain_df = stock_gain_df.set_index("date")
    equity_ticker = equity_list[equity_list.Name.isin(
        equity_name)].Ticker.tolist()

    stock_gain_df = stock_gain_df.loc[:, equity_ticker]

    fig = go.Figure()
    for i, e_name in enumerate(equity_name):
        fig.add_trace(go.Scatter(x=stock_gain_df.index,
                                 y=stock_gain_df[equity_ticker[i]], mode="lines", name=e_name))
    st.plotly_chart(fig, use_container_width=True)


def main():
    df = load_data(equity_list)

    sl_initial_amount = 10000
    st.sidebar.markdown("### Set parameters for simulation")
    sl_leverage = st.sidebar.slider('Leverage', 0.0, 1.0, 1.0)
    sl_start_dt = st.sidebar.date_input(
        'Choose investment start date', date(
            start_date_year, start_date_month, start_date_day),
        date(start_date_year, start_date_month, start_date_day))
    sl_end_dt = st.sidebar.date_input(
        'Choose investment end date', (end_date - timedelta(days=2)),
        date(start_date_year, start_date_month, start_date_day))

    sl_select_tickers = st.sidebar.multiselect("Select tickers to compare performance",
                                               equity_list.Name.tolist(),
                                               equity_list.Name.tolist()[:3])

    if (np.datetime64(sl_start_dt) > np.datetime64(sl_end_dt)):
        st.write(f"""
        _Error: Start Date greater than End Date_
        * Investment Start Date = {sl_start_dt}
        * Investment End Date = {sl_end_dt}

        Please fix the dates before proceeding
        """
                 )

    elif (np.datetime64(sl_start_dt) < (date(
            start_date_year, start_date_month, start_date_day))):
        st.write(f"""
                 _Error: Please select a later start date_
                 * Investment Start Date={sl_start_dt}
                 * Possible Start Date={start_date}

                 Please fix the dates before proceeding
                """
                 )

    elif (np.datetime64(sl_end_dt) > np.datetime64(end_date)):
        st.write(f"""
        _Error: End Date should be yesterday or earlier_
        * Investment End Date = {sl_end_dt}

        Please fix the dates before proceeding
        """
                 )

    else:
        df_slice = df.loc[(df.index >= np.datetime64(sl_start_dt)) & (
            df.index <= np.datetime64(sl_end_dt))]

        st.write(f"""
        ### Parameters

        * Initial Amount = {locale.currency(sl_initial_amount, grouping=True)}
        * Leverage = {sl_leverage}
        * Investment Start Date = {sl_start_dt}
        * Investment End Date = {sl_end_dt}
        """)

        # cleanup data for adjusted change values
        stock_analyze_df = df_slice.iloc[:, :len(equity_list)].copy()
        stock_analyze_df.columns = stock_analyze_df.columns.droplevel()
        stock_analyze_df = stock_analyze_df.fillna(
            method="ffill", inplace=False)

        # calc change percentage
        stock_analyze_pc_df = stock_analyze_df.apply(
            lambda x: (x - x.shift(1))/x.shift(1))
        stock_analyze_pc_df = stock_analyze_pc_df.fillna(0)

        # run simulation on button press
        if st.sidebar.button("Run Simulation", "run-exp-btn"):
            gain_data = run_experiment(
                sl_initial_amount, sl_leverage, stock_analyze_pc_df)
            stock_gain_df = pd.DataFrame(gain_data)
            stock_gain_df["date"] = stock_analyze_pc_df.index

            with st.spinner("Running Simulation..."):
                plot_avgs(stock_gain_df, sl_select_tickers)
            # plot_df(sl_select_tickers)

                st.write("""
                [Try our random events simulator to understand ergodicity better](https://sleepy-ocean-52778.herokuapp.com/)
                """)


if __name__ == "__main__":
    main()
