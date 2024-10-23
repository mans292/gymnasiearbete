import pandas as pd
# Assuming 'column_name' is the column from which you want to remove the bottom 2%
column_name = 'slutpris'  # Replace with the actual column name

# Load your dataset
file = 'lägenheter_med_koordinater_slutgiltig.xlsx'
df = pd.read_excel(file)

# Calculate the 2nd percentile
lower_percentile = df[column_name].quantile(0.02)

# Filter out rows where the values are less than the 2nd percentile
df_filtered = df[df[column_name] >= lower_percentile]

# Save the filtered dataset to a new Excel file
df_filtered.to_csv('filtrerade_lägenheter.csv', index=False)