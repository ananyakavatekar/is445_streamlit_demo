import pandas as pd
import streamlit as st
import altair as alt

data = pd.read_csv("https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv")

st.title("Illinois Building Composition")

st.write("This report explores the distribution and attributes of buildings in Illinois")

# viz 1: Dist of buildings by county

st.header("Building Count by County in Illinois")

building_count_by_county = data["County"].value_counts().reset_index()

# naming cols to make it easier to call later
building_count_by_county.columns = ["County", "Count"]


# number of counties (top to bottom)
num_counties = building_count_by_county.shape[0]
county_count = st.slider("Number of Counties: ", 1, num_counties, 10)

counties_to_show = building_count_by_county.head(county_count)

viz_1 = alt.Chart(counties_to_show).mark_bar(color="steelblue").encode(
    x=alt.X("Count:Q", title="Building Count"),
    y=alt.Y("County:N", sort="-x", title="County"),
    tooltip=["County", "Count"]
).properties(
    title="Number of Buildings by County"
)

st.altair_chart(viz_1)


st.write("""
The visualization above showcases the distribution of buildings in Illinois based on the county they are located in.
I chose to make the visualization a horizontal bar graph so that building counts by county would be easier to compare and there
is adequate space for the county names. I made the color a simple blue so that users can focus on the relative differences in building counts.
The interactive element added to this visualization is a slider that allows viewers to alter the
number of counties whose building counts are showcased. I made the minimum county count 1 and the maximum the total number
of counties and the default county count is 10.
If I had more time, I would add a feature that allows users to select specific counties to compare.
""")

# viz 2 building construction by decade

st.header("Number of Buildings Constructed by Decade in Illinois.")

# make sure construction years are numeric
data["Year Constructed"] = pd.to_numeric(data["Year Constructed"], errors="coerce")

years = data[data["Year Constructed"].between(1800, 2026)].copy()

# group years into decades
years["Decade"] = (years["Year Constructed"] // 10 * 10).astype(int)

# count buildings by decade
building_count_by_decade = years["Decade"].value_counts().sort_index().reset_index()

building_count_by_decade.columns = ["Decade", "Count"]

viz_2 = alt.Chart(building_count_by_decade).mark_line(
    point=True, color="steelblue"
).encode(
    x=alt.X("Decade:Q", title="Construction Decade"),
    y=alt.Y("Count:Q", title="Building Count"),
    tooltip=["Decade", "Count"]
).properties(
    title="Number of Buildings Constructed by Decade"
)

st.altair_chart(viz_2)

st.write("""
The visualization above showcases the number of buildings in the Illinois Building Inventory constructed by decade.
I did this by grouping the construction year variable into decade intervals and then mapping it onto a line chart.
I chose a line chart particularly because it helps highlight the overall trend across time (whether there was
growth, decline, or stagnation in the construction count).
I once again made this visualization a simple blue so viewers can focus on interpreting the trend.
For future versions, I would add a dropdown to allow users to compare the construction trend based by county.
""")
