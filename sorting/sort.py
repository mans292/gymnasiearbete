import pandas as pd
import re
import math


# Step 1: Load the two Excel files into DataFrames
file1 = 'test4.xlsx'  # Replace with your actual file paths
file2 = 'test5.xlsx'

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)


combined_df = pd.concat([df1, df2])

combined_df = combined_df.sort_values(by='postnummer')



def clean_price(value):
    if value != 'N/A':
        val = str(value).replace('m²', '')
        final_val = str(val).replace('\xa0', '')
        final_val = final_val.replace(',','.')
        if 'ha' in final_val:
            final_val = final_val.replace('ha', '')
            return float(final_val) * 10000
        elif math.isnan(float(final_val)):
            return 0
        else:
            return final_val
def clean_price2(value):
    val = str(value).replace('kr/år', '')
    final_val = str(val).replace('\xa0', '')
    if math.isnan(float(final_val)):
        return value
    else:
        return float(final_val)


combined_df['Boarea'] = combined_df['Boarea'].apply(clean_price)
combined_df['Biarea'] = combined_df['Biarea'].apply(clean_price)
combined_df['Tomtarea'] = combined_df['Tomtarea'].apply(clean_price)
combined_df['Driftkostnad'] = combined_df['Driftkostnad'].apply(clean_price2)


# Step 5: Save the combined, cleaned data into a new Excel file
combined_df.to_excel('houses2.xlsx', index=False)

print("Data combined, sorted, and cleaned successfully.")