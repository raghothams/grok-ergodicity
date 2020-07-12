import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns
import plotly.express as px

st.write("""
# Random Event & Ergodicity

### A lesson on Ergodicity with random events
""")

np.random.seed(9)

def run_experiment(initial_amount, gain_pct, loss_pct, leverage):
    # num of time steps
    t_N = 60

    # num of people
    p_N = 100000

    evt_data = {}
    gain_data = {}

    data_load_state = st.text('Running Experiment ...')

    # generate data for every person
    for i in range(p_N):
        # start with initial amount as leverage
        person_gain = initial_amount
        
        # generate random events of gain / loss for N time steps
        evts = np.random.randint(0,2, t_N)
        
        # temp state store for interim gains
        gains = [person_gain]
        
        # calc gain progression
        for e in evts:
            if e == 0:
                person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 - loss_pct))
            else:
                person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 + gain_pct))
            
            gains.append(person_gain)

    #         print(person_gain, e)
            
        # append gain data - events, gain progression, to a dictionary
        evt_data[f"p_evt_{i+1}"] = evts
        gain_data[f"p_gain_{i+1}"] = gains

    df_gain = pd.DataFrame(gain_data)
    df_gain = df_gain.reset_index()

    df_ens = pd.DataFrame()
    df_ens["ens_avg"] = df_gain.apply(np.mean, axis=1)
    df_ens["ens_med"] = df_gain.apply(np.median, axis=1)
    df_ens = df_ens.reset_index()

    data_load_state.text('Experiment Completed!')


    st.write("""
    ## Ensemble Average
    """)
    fig = px.line(df_ens, x="index", y="ens_avg")
    fig.update_layout(
        xaxis_title="timestep",
        yaxis_title="ensemble avg. at timestep",)
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    ## Specific case (Reality)
    """)
    rand_p = np.random.randint(1, 100000)
    fig = px.line(df_gain, x="index", y="p_gain_100")
    fig.update_layout(
        xaxis_title="timestep",
        yaxis_title="gain at timestep",)
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    ## Histogram of money people end up with
    """)
    residue = df_gain.iloc[-1].value_counts().reset_index()
    fig = px.histogram(residue, x="index", marginal="box")
    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    [Try our stock market usecase to understand ergodicity better](https://stark-sierra-25548.herokuapp.com/)
    """)

sl_initial_amount = st.sidebar.slider('Initial Amount', 1000, 1000000, 1000)
sl_gain_pct = st.sidebar.slider('Gain %', 0.0, 1.0, 0.5)
sl_loss_pct = st.sidebar.slider('Loss %', 0.0, 1.0, 0.4)
sl_leverage = st.sidebar.slider('Leverage', 0.0, 1.0, 1.0)

st.write(f"""
## Experiment Parameters

* Initial Amount = ${sl_initial_amount}
* Gain = {sl_gain_pct}
* Loss = {sl_loss_pct}
* Leverage = {sl_leverage}
* Time Steps = 60
* Number of Sequences = 100,000
""")

if st.sidebar.button("Run Experiment", "run-exp-btn"):
    run_experiment(sl_initial_amount, sl_gain_pct, sl_loss_pct, sl_leverage)


