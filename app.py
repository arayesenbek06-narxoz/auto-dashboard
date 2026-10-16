import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auto dashboard", layout="wide")

# Load the data once and prepare readable columns
@st.cache_data
def load_data():
    df = pd.read_csv("auto.csv")
    df["origin_name"] = df["origin"].map({1: "USA", 2: "Europe", 3: "Japan"})
    df["model_year"] = df["year"] + 1900
    return df

df = load_data()

st.title("What drives fuel efficiency? Auto dataset, 1970-1982")
st.write("Question: how are weight, horsepower and region of origin related to mpg, and how did this change over the years?")

# Filters in the sidebar: region and model year range
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region of origin", ["USA", "Europe", "Japan"],
                                 default=["USA", "Europe", "Japan"])
years = st.sidebar.slider("Model year", 1970, 1982, (1970, 1982))

# All four charts use the same filtered table, so they change together
filtered = df[df["origin_name"].isin(regions) & df["model_year"].between(years[0], years[1])]

if filtered.empty:
    st.warning("No cars match the selected filters.")
    st.stop()

# Key numbers for the selected cars
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cars", len(filtered))
c2.metric("Average mpg", round(filtered["mpg"].mean(), 2))
c3.metric("Average horsepower", round(filtered["horsepower"].mean(), 1))
c4.metric("Average weight (lb)", round(filtered["weight"].mean(), 0))

# Row 1: scatter plot (weight vs mpg) and histogram of mpg
left, right = st.columns(2)
with left:
    fig1 = px.scatter(filtered, x="weight", y="mpg", color="origin_name", size="horsepower",
                      hover_name="name", title="Weight vs mpg (bubble size = horsepower)")
    st.plotly_chart(fig1, use_container_width=True)
with right:
    fig2 = px.histogram(filtered, x="mpg", color="origin_name", nbins=20,
                        title="Distribution of mpg")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: boxplot by region and line chart of average mpg by year
left2, right2 = st.columns(2)
with left2:
    fig3 = px.box(filtered, x="origin_name", y="mpg", color="origin_name",
                  title="mpg by region of origin")
    st.plotly_chart(fig3, use_container_width=True)
with right2:
    by_year = filtered.groupby(["model_year", "origin_name"], as_index=False)["mpg"].mean()
    fig4 = px.line(by_year, x="model_year", y="mpg", color="origin_name", markers=True,
                   title="Average mpg by model year")
    st.plotly_chart(fig4, use_container_width=True)
