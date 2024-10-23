import pandas as pd

file = 'excel/houses_to_sort.xlsx'

df = pd.read_excel(file)

def clean_rum(value):
    val = str(value).replace('rum', '')
    val = val.replace('\xa0', '')
    val = val.replace(',', '.')
    
    return float(val)

clean_df = df.dropna(subset=['Driftkostnad', 'Antal_rum', 'medelinkomst_månad', 'Boarea', 'Biarea', 'Tomtarea',])

    
    # Remove rows where all values are missing (completely empty rows)

clean_df = clean_df.dropna(how='all')


clean_df['Antal_rum'] = clean_df['Antal_rum'].apply(clean_rum)
print(clean_df)

clean_df.to_excel('final_houses.xlsx', index=False)
clean_df.to_csv('final_houses.csv', index=False)
print('klar din fitta')

