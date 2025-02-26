import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG data exploration")

@st.cache_data #decorator
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="./data/raw/mpg.csv") #for speed
mpg_df = deepcopy(mpg_df_raw) #for security, you cannot change what is cached

# First some MPG Data Exploration
#mpg_df = pd.read_csv("./data/raw/mpg.csv")
#st.table(data=mpg_df)
st.subheader("My raw dataset")

if st.checkbox("show dataframe"):
    st.dataframe(data=mpg_df)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("data source:", url)

left_column, right_column = st.columns(2)

years=["All"]+sorted(pd.unique(mpg_df['year']))
year=left_column.selectbox("Select one of the years", years, index=2)

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

show_means = right_column.radio(
    label='Show Class Means', options=['Yes', 'No'])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

means = reduced_df.groupby('class').mean(numeric_only=True)

m_fig, ax = plt.subplots(figsize=(10, 8))
if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="Class Means")
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

#st.pyplot(m_fig)

# In Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers",
                               marker=dict(color="red")))  # ✅ Correct placement of color

    p_fig.update_layout(showlegend=False)

p_fig.update_layout(title_font_size=22)
#st.plotly_chart(p_fig)

if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)


# Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()

ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']

st.map(ds_geo)