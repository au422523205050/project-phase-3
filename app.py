import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import os
st.set_page_config(layout="wide")
st.title("Property Theft and Recovery Analysis")
data_path = "data/property_stolen_recovered_tableau.csv"  # Update if needed
if not os.path.exists(data_path):
    st.error(f"Data file not found at `{data_path}`.")
    st.stop()
data = pd.read_csv(data_path)
st.sidebar.header("Filter Options") 
selected_state = st.sidebar.selectbox("Select a State/UT", ["All"] + sorted(data['State/UT'].unique())) 
selected_year = st.sidebar.selectbox("Select a Year", ["All"] + sorted(data['Year'].unique()))
filtered_data = data.copy() 
if selected_state != "All": 
    filtered_data = filtered_data[filtered_data['State/UT'] == selected_state] 
if selected_year != "All": 
    filtered_data = filtered_data[filtered_data['Year'] == int(selected_year)]
st.subheader("Filtered Dataset") 
st.dataframe(filtered_data)
st.subheader("Summary Metrics") 
total_stolen = filtered_data['Value_of_Property_Stolen'].sum() 
total_recovered = filtered_data['Value_of_Property_Recovered'].sum() 
recovery_rate = (total_recovered / total_stolen * 100) if total_stolen > 0 else 0
col1, col2, col3 = st.columns(3) 
col1.metric("Total Value Stolen", f"₹{total_stolen:,.0f}") 
col2.metric("Total Value Recovered", f"₹{total_recovered:,.0f}") 
col3.metric("Recovery Rate", f"{recovery_rate:.2f}%")
st.subheader("State-wise Recovery Comparison") 
if selected_year != "All": 
    chart_data = data[data['Year'] == int(selected_year)] 
else: 
    chart_data = data
chart_data = chart_data.groupby('State/UT').agg({
    'Value_of_Property_Stolen': 'sum',
    'Value_of_Property_Recovered': 'sum'
}).reset_index()
fig, ax = plt.subplots(figsize=(12, 6)) 
chart_data.set_index('State/UT')[['Value_of_Property_Stolen', 'Value_of_Property_Recovered']]\
    .sort_values(by='Value_of_Property_Stolen', ascending=False)\
    .head(10).plot(kind='bar', ax=ax)
plt.ylabel("Value (₹)") 
plt.title("Top 10 States by Value of Property Stolen vs Recovered") 
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)
st.markdown("---") 
st.caption("Data source: Property Stolen and Recovered Dataset")
