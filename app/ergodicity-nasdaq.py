from datetime import date, datetime 
import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns
import plotly.express as px

st.write("""
# Ergodicity Experiment
""")

np.random.seed(9)

@st.cache
def load_data():
    df = pd.read_csv("../data/clean_nasdaq.csv")
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.normalize()

    return df

def run_experiment(initial_amount, leverage, df):
    # num of time steps
    t_N = 60

    df = df.reset_index().drop("index", axis=1)
    # num of people
    p_N = 100000

    evt_data = {}
    gain_data = {}

    data_load_state = st.text('Running Experiment ...')

    # generate data for every person
    # start with initial amount as leverage
    person_gain = initial_amount
    
    # temp state store for interim gains
    gains = [person_gain]
    
    # calc gain progression
    for i in range(df.shape[0]):
        row = df.iloc[i]
        person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 + row["change_frac"]))
        
        gains.append(person_gain)

#         print(person_gain, e)
        

    df_gain = pd.DataFrame(gains)
    df_gain = df_gain.reset_index()
    df_gain.columns = ["index", "gain"]
    df_gain["ts"] = df["DATE"]

    # df_ens = pd.DataFrame()
    # df_ens["ens_avg"] = df_gain.apply(np.mean, axis=1)
    # df_ens["ens_med"] = df_gain.apply(np.median, axis=1)
    # df_ens = df_ens.reset_index()

    data_load_state.text('Experiment Completed!')


    st.write("""
    ## Ensemble Average
    """)
    fig = px.line(df_gain, x="ts", y="gain")
    fig.update_layout(
        xaxis_title="timestep",
        yaxis_title="ensemble avg. at timestep",)
    st.plotly_chart(fig, use_container_width=True)

    # st.write("""
    # ## Specific case (Reality)
    # """)
    # rand_p = np.random.randint(1, 100000)
    # fig = px.line(df_gain, x="index", y="p_gain_100")
    # fig.update_layout(
    #     xaxis_title="timestep",
    #     yaxis_title="gain at timestep",)
    # st.plotly_chart(fig, use_container_width=True)

    # st.write("""
    # ## Histogram of money people end up with
    # """)
    # residue = df_gain.iloc[-1].value_counts().reset_index()
    # fig = px.histogram(residue, x="index", marginal="box")
    # st.plotly_chart(fig, use_container_width=True)


def main():
    df = load_data()

    sl_initial_amount = st.slider('Initial Amount', 1000, 1000000, 1000)
    # sl_gain_pct = st.slider('Gain %', 0.0, 1.0, 0.5)
    # sl_loss_pct = st.slider('Loss %', 0.0, 1.0, 0.4)
    sl_leverage = st.slider('Leverage', 0.0, 1.0, 1.0)
    sl_start_dt = st.date_input('Choose investment start date', value=date(1995,1,10))
    sl_end_dt = st.date_input('Choose investment end date', value=date(2020, 1, 31))

    st.write(sl_start_dt)
    st.write(sl_end_dt)
    df_slice = df.loc[(df["DATE"] >= np.datetime64(sl_start_dt)) & (df["DATE"] <= np.datetime64(sl_end_dt))]
    st.write(df_slice.head())

    st.write(f"""
    ## Experiment Parameters

    * Initial Amount = ${sl_initial_amount}
    * Leverage = {sl_leverage}
    """)

    if st.button("Run", "run-exp-btn"):
        run_experiment(sl_initial_amount, sl_leverage, df_slice)

    # initial_amount = 1000
    # gain_pct = 0.5
    # loss_pct = 0.4
    # leverage = 1.0



    # fig.show()
    # sns.lineplot(x=df_ens.index, y=df_ens["ens_avg"], )

    # sns.lineplot(x=df_gain.index, y=df_gain["p_gain_100"])

if __name__ == "__main__":
    main()