import os
import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "cleaned_disaster_data.csv"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Disaster Historical Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        DATA_FILE,
        encoding="utf-8"
    )

    return df


try:

    df = load_data()

except Exception as e:

    st.error(
        f"Unable to load disaster dataset:\n\n{e}"
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 Historical Disaster Analytics"
)

st.markdown(
    """
    Analysis of historical disaster events using the
    EMDAT-based cleaned disaster dataset.
    """
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# Year filter

if "Start Year" in df.columns:

    min_year = int(df["Start Year"].min())
    max_year = int(df["Start Year"].max())

    selected_years = st.sidebar.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    filtered_df = df[
        (df["Start Year"] >= selected_years[0]) &
        (df["Start Year"] <= selected_years[1])
    ].copy()

else:

    filtered_df = df.copy()


# Disaster type filter

if "Disaster Type" in filtered_df.columns:

    disaster_types = sorted(
        filtered_df["Disaster Type"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_types = st.sidebar.multiselect(
        "Disaster Type",
        disaster_types,
        default=disaster_types
    )

    if selected_types:

        filtered_df = filtered_df[
            filtered_df["Disaster Type"].isin(
                selected_types
            )
        ]


# Country filter

if "Country" in filtered_df.columns:

    countries = sorted(
        filtered_df["Country"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_countries = st.sidebar.multiselect(
        "Country",
        countries,
        default=[]
    )

    if selected_countries:

        filtered_df = filtered_df[
            filtered_df["Country"].isin(
                selected_countries
            )
        ]


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Disaster Statistics")


total_events = len(filtered_df)


total_deaths = 0

if "Total Deaths" in filtered_df.columns:

    total_deaths = pd.to_numeric(
        filtered_df["Total Deaths"],
        errors="coerce"
    ).fillna(0).sum()


total_affected = 0

if "Total Affected" in filtered_df.columns:

    total_affected = pd.to_numeric(
        filtered_df["Total Affected"],
        errors="coerce"
    ).fillna(0).sum()


total_damage = 0

if "Total Damage ('000 US$)" in filtered_df.columns:

    total_damage = pd.to_numeric(
        filtered_df["Total Damage ('000 US$)"],
        errors="coerce"
    ).fillna(0).sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Disaster Events",
        f"{total_events:,}"
    )


with col2:

    st.metric(
        "Total Deaths",
        f"{int(total_deaths):,}"
    )


with col3:

    st.metric(
        "People Affected",
        f"{int(total_affected):,}"
    )


with col4:

    st.metric(
        "Reported Damage",
        f"{int(total_damage):,}"
    )


st.divider()


# ============================================================
# DISASTER TYPE DISTRIBUTION
# ============================================================

if "Disaster Type" in filtered_df.columns:

    st.subheader(
        "🌪️ Disaster Type Distribution"
    )

    type_counts = (
        filtered_df["Disaster Type"]
        .value_counts()
        .reset_index()
    )

    type_counts.columns = [
        "Disaster Type",
        "Number of Events"
    ]

    fig = px.bar(
        type_counts,
        x="Disaster Type",
        y="Number of Events",
        title="Number of Disaster Events by Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# YEARLY TREND
# ============================================================

if "Start Year" in filtered_df.columns:

    st.subheader(
        "📈 Yearly Disaster Trend"
    )

    yearly = (
        filtered_df
        .groupby("Start Year")
        .size()
        .reset_index(
            name="Number of Events"
        )
    )

    fig = px.line(
        yearly,
        x="Start Year",
        y="Number of Events",
        markers=True,
        title="Disaster Events by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# COUNTRY ANALYSIS
# ============================================================

if "Country" in filtered_df.columns:

    st.subheader(
        "🌍 Countries with Most Disaster Events"
    )

    country_counts = (
        filtered_df["Country"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    country_counts.columns = [
        "Country",
        "Number of Events"
    ]

    fig = px.bar(
        country_counts,
        x="Number of Events",
        y="Country",
        orientation="h",
        title="Top 15 Countries by Disaster Events"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DEATHS BY DISASTER TYPE
# ============================================================

if (
    "Disaster Type" in filtered_df.columns
    and "Total Deaths" in filtered_df.columns
):

    st.subheader(
        "⚠️ Deaths by Disaster Type"
    )

    death_data = filtered_df.copy()

    death_data["Total Deaths"] = pd.to_numeric(
        death_data["Total Deaths"],
        errors="coerce"
    ).fillna(0)

    deaths_by_type = (
        death_data
        .groupby("Disaster Type")["Total Deaths"]
        .sum()
        .reset_index()
        .sort_values(
            "Total Deaths",
            ascending=False
        )
    )

    fig = px.bar(
        deaths_by_type,
        x="Disaster Type",
        y="Total Deaths",
        title="Total Deaths by Disaster Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AFFECTED PEOPLE BY YEAR
# ============================================================

if (
    "Start Year" in filtered_df.columns
    and "Total Affected" in filtered_df.columns
):

    st.subheader(
        "👥 People Affected Over Time"
    )

    affected_data = filtered_df.copy()

    affected_data["Total Affected"] = pd.to_numeric(
        affected_data["Total Affected"],
        errors="coerce"
    ).fillna(0)

    affected_year = (
        affected_data
        .groupby("Start Year")["Total Affected"]
        .sum()
        .reset_index()
    )

    fig = px.area(
        affected_year,
        x="Start Year",
        y="Total Affected",
        title="Total People Affected by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DATA TABLE
# ============================================================

st.subheader(
    "📋 Filtered Disaster Records"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Disaster NLP Intelligent System | Historical Disaster Analytics"
)
