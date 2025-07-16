import streamlit as st  # Make sure streamlit is installed: pip install streamlit
import json
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="OperatorOS Leadscore API - Usage Analytics", layout="centered")

st.title("📊 OperatorOS API Usage Dashboard")
st.write("Live analytics from usage.log (last 1000 events).")

log_path = Path("usage.log")
if not log_path.exists():
    st.error("No usage.log file found. Make sure logging is enabled.")
    st.stop()

# Read and parse log entries
entries = []
with open(log_path) as f:
    for line in f:
        try:
            entry = json.loads(line)
            entries.append(entry)
        except Exception:
            continue

if not entries:
    st.warning("No events logged yet.")
    st.stop()

df = pd.DataFrame(entries)
df['timestamp'] = pd.to_datetime(df['timestamp'])

st.metric("Total Calls", len(df))
st.metric("Unique API Keys", df['api_key'].nunique())

st.write("### Last 10 Events")
st.dataframe(df.sort_values('timestamp', ascending=False).head(10))

st.write("### All Usage (Chronological)")
st.dataframe(df.sort_values('timestamp', ascending=True))

st.write("### API Key Usage Counts")
st.bar_chart(df['api_key'].value_counts())

st.write("### Traffic by Client IP")
st.bar_chart(df['client_ip'].value_counts())

st.write("### Recent Activity Timeline")
st.line_chart(df.set_index('timestamp').resample('10min').size())
