import streamlit as st
import pandas as pd

st.set_page_config(page_title="STL LIVE", layout="wide")

# --------------------------
# SIDEBAR (CONTROL LAYER)
# --------------------------
st.sidebar.title("STL Navigation")

page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Blueprint", "Tracking", "Control Layer"]
)

st.sidebar.subheader("Live Controls")

input_mode = st.sidebar.radio(
    "Input Mode",
    ["Manual", "Demo Data", "Upload CSV"]
)

auto_refresh = st.sidebar.checkbox("Auto Refresh")

refresh_rate = st.sidebar.slider("Refresh every (sec)", 5, 60, 10)

# --------------------------
# DATA INPUT
# --------------------------

def get_manual_data():
    st.subheader("Manual Input")

    store_visitors = st.number_input("Store Visitors", value=2000)
    online_visitors = st.number_input("Online Visitors", value=10000)
    market_visitors = st.number_input("Marketplace Visitors", value=3000)

    store_purchases = st.number_input("Store Purchases", value=400)
    online_purchases = st.number_input("Online Purchases", value=200)
    market_purchases = st.number_input("Marketplace Purchases", value=90)

    store_revenue = st.number_input("Store Revenue", value=12000)
    online_revenue = st.number_input("Online Revenue", value=8000)
    market_revenue = st.number_input("Marketplace Revenue", value=4500)

    data = pd.DataFrame({
        "channel": ["Store", "Online", "Marketplace"],
        "visitors": [store_visitors, online_visitors, market_visitors],
        "purchases": [store_purchases, online_purchases, market_purchases],
        "revenue": [store_revenue, online_revenue, market_revenue]
    })

    return data


def get_demo_data():
    data = pd.DataFrame({
        "channel": ["Store", "Online", "Marketplace"],
        "visitors": [2000, 10000, 3000],
        "purchases": [400, 200, 90],
        "revenue": [12000, 8000, 4500]
    })
    return data


def get_csv_data():
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:", df)
        return df
    return None


# --------------------------
# SELECT DATA SOURCE
# --------------------------

if input_mode == "Manual":
    df = get_manual_data()

elif input_mode == "Demo Data":
    df = get_demo_data()

elif input_mode == "Upload CSV":
    df = get_csv_data()

else:
    df = None


# --------------------------
# ENGINE (PROCESSING)
# --------------------------

def run_stl_engine(df):
    df["conversion"] = df["purchases"] / df["visitors"]

    total_revenue = df["revenue"].sum()
    conversion_rate = df["conversion"].mean()

    weakest_channel = df.loc[df["conversion"].idxmin()]["channel"]

    stl_score = round(conversion_rate, 2)

    return total_revenue, conversion_rate, weakest_channel, stl_score


# --------------------------
# DASHBOARD (INTELLIGENCE)
# --------------------------

if df is not None and page == "Dashboard":

    st.title("STL LIVE — Structured Intelligence Engine")

    total_revenue, conversion_rate, weakest, stl_score = run_stl_engine(df)

    st.subheader("System Health")

    col1, col2, col3 = st.columns(3)

    col1.metric("STL LIVE", stl_score)
    col2.metric("Total Revenue", f"${total_revenue}")
    col3.metric("Conversion %", f"{round(conversion_rate * 100, 2)}%")

    st.write(f"⚠️ Weakest Channel: **{weakest}**")

    if conversion_rate < 0.05:
        st.error("🚨 Low conversion detected")

    st.subheader("Channel Performance")
    st.dataframe(df)

    st.bar_chart(df.set_index("channel")["revenue"])


# --------------------------
# BLUEPRINT (ARCHITECTURE)
# --------------------------

elif page == "Blueprint":
    st.title("STL Blueprint")

    st.write("""
    Applications → Pipelines → Storage → Intelligence

    STL Flow:
    - Understood (Input)
    - Hallow (Observation)
    - Honor (Processing)
    - Higher (Storage)
    - Hunter (Decision)
    """)


# --------------------------
# TRACKING (MONITORING)
# --------------------------

elif page == "Tracking":
    st.title("Tracking")

    if df is not None:
        st.write("Live Data Snapshot")
        st.dataframe(df)


# --------------------------
# CONTROL LAYER
# --------------------------

elif page == "Control Layer":
    st.title("Control Layer")

    st.write(f"Input Mode: {input_mode}")
    st.write(f"Auto Refresh: {auto_refresh}")
    st.write(f"Refresh Rate: {refresh_rate} sec")
