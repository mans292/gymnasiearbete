import pandas as pd
import re
import math


# Step 1: Load the two Excel files into DataFrames
file1 = 'Lägenheter_med_koordinater_komplettering.xlsx'  # Replace with your actual file paths


df1 = pd.read_excel(file1)


combined_df = df1

combined_df = combined_df.sort_values(by='postnummer')

clean_df = combined_df.dropna(subset=['Våning', 'Antal rum', 'medelinkomst_månad', 'Boarea', 'Avgift'])

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
        return 3000
    else:
        return float(final_val)
    
def clean_level(df):
    df['Finns_hiss'] = 0
    for index, row in df.iterrows():
        if 'hiss' in str(row['Våning']):
            if 'finns inte' in str(row['Våning']):
                df.at[index, 'Finns_hiss'] = 0
            else:
                df.at[index, 'Finns_hiss'] = 1
        value = str(row['Våning'])[0:1]
        if value == '-':
            value = str(row['Våning'])[0:2]
        df.at[index, 'Våning'] = float(value)
        
def clean_uteplats(value):
    if value == 'Ja':
        return 1
    else:
        return 0
def clean_rum(value):
    val = str(value).replace('rum', '')
    val = val.replace('\xa0', '')
    val = val.replace(',', '.')
    
    return float(val)


clean_df['Boarea'] = clean_df['Boarea'].apply(clean_price)
clean_df['Uteplats'] = clean_df['Uteplats'].apply(clean_uteplats)
clean_df['Driftkostnad'] = clean_df['Driftkostnad'].apply(clean_price2)
clean_df['Antal rum'] = clean_df['Antal rum'].apply(clean_rum)
clean_level(clean_df)

# Step 5: Save the combined, cleaned data into a new Excel file
clean_df.to_excel('Lägenheter_med_koordinater_komplettering3.xlsx', index=False)

print("Data combined, sorted, and cleaned successfully.")