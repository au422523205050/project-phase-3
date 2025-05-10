import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px
data = pd.read_csv('data/10_Property_stolen_and_recovered.csv')
data.dropna(inplace=True) 
data.columns = [col.strip().replace(" ", "_").upper() for col in data.columns]
data['VALUE_OF_PROPERTY_STOLEN'] = pd.to_numeric(data['VALUE_OF_PROPERTY_STOLEN'], errors='coerce') 
data['VALUE_OF_PROPERTY_RECOVERED'] = pd.to_numeric(data['VALUE_OF_PROPERTY_RECOVERED'], errors='coerce')
plt.figure(figsize=(10,5)) 
sns.histplot(data['VALUE_OF_PROPERTY_STOLEN'], bins=30, kde=True) 
plt.title('Distribution of Property Stolen Value') 
plt.xlabel('Value (in INR)') plt.ylabel('Frequency') 
plt.tight_layout() 
plt.savefig("output/property_stolen_distribution.png")
plt.figure(figsize=(12,8)) 
data_state = data.groupby('STATE/UT')[['VALUE_OF_PROPERTY_STOLEN','VALUE_OF_PROPERTY_RECOVERED']].sum().sort_values(by='VALUE_OF_PROPERTY_STOLEN', ascending=False) 
data_state.plot(kind='bar', figsize=(14,6)) plt.title('Total Property Stolen vs Recovered by State') 
plt.xlabel('State/UT') 
plt.ylabel('Value in INR') 
plt.tight_layout() 
plt.savefig("output/statewise_comparison.png")
data['RECOVERY_RATE'] = (data['VALUE_OF_PROPERTY_RECOVERED'] / data['VALUE_OF_PROPERTY_STOLEN']) * 100 
avg_recovery = data.groupby('STATE/UT')['RECOVERY_RATE'].mean().sort_values(ascending=False)
fig = px.bar(avg_recovery.reset_index(), x='STATE/UT', y='RECOVERY_RATE', title='Average Recovery Rate by State/UT') 
fig.write_html("output/interactive_recovery_rate.html")
print("Analysis Complete. Outputs saved in 'output' directory.")
