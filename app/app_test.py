import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns
import plotly.express as px

st.write("""
# Ergodicity Experiment
""")

np.random.seed(10)

st.write("""
## Experiment Parameters

* Initial Amount = $1000
* Gain = 50%
* Loss = 40%
* Leverage = 1
* Time Steps = 60
* Number of Sequences = 100,000
""")

initial_amount = 1000
gain_pct = 0.5
loss_pct = 0.4
leverage = 1.0

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
    gains = []
    
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
st.plotly_chart(fig, use_container_width=True)

st.write("""
## Specific case (Reality)
""")
fig = px.line(df_gain, x="index", y="p_gain_10")
st.plotly_chart(fig, use_container_width=True)

# fig.show()
# sns.lineplot(x=df_ens.index, y=df_ens["ens_avg"], )

# sns.lineplot(x=df_gain.index, y=df_gain["p_gain_100"])