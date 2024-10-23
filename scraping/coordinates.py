import requests
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Read your Excel file
file = 'koordinater2.xlsx'
df = pd.read_excel(file)

# Function to get coordinates from Google Geocoding API
def get_coordinates(gata, nummer, postnummer, api_key):
    address = f'{gata} {nummer}, {postnummer}'
    google_api_link = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    
    # Setting up retry strategy for connection errors
    retry_strategy = Retry(
        total=5,  # Total retries
        backoff_factor=1,  # Exponential backoff
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP statuses
        method_whitelist=["GET"]  # Retry for GET requests only
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        # Send request to Google Geocoding API with a timeout
        response = http.get(google_api_link, timeout=10)
        response_json = response.json()

        # Check if the response contains results
        if response_json['status'] == 'OK':
            lat = response_json['results'][0]['geometry']['location']['lat']
            lng = response_json['results'][0]['geometry']['location']['lng']
            print(lat, lng)
            return lat, lng
        else:
            print('nej')
            return None, None
    except Exception as e:
        df.to_excel('Lägenheter_med_koordinater.xlsx', index=False)
        print(f"Error occurred for address {address}: {e}")
        return None, None

# Add new columns for latitude and longitude
df['latitude'] = None
df['longitude'] = None

# Define your Google API Key
api_key = 'AIzaSyA04BO-hlMU_qHr4jR2eIbltbG4-YB8j3c'

# Loop through each row in the DataFrame
try:
    for index, row in df.iterrows():
        gata = row['gata']
        nummer = row['nummer']
        postnummer = row['postnummer']
        
        # Get coordinates
        lat, lng = get_coordinates(gata, nummer, postnummer, api_key)
        
        # Update the DataFrame with coordinates
        df.at[index, 'latitude'] = lat
        df.at[index, 'longitude'] = lng
        time.sleep(0.041)
except Exception as e:
    # If any error occurs, save the current DataFrame to an Excel file
    print(f"An error occurred during processing: {e}")
    df.to_excel('Lägenheter_med_koordinater.xlsx', index=False)
    print("Progress saved to 'koordinater_with_coords_on_error.xlsx' due to error.")
    raise  # Re-raise the error after saving so it's still visible

# If no errors occur, save the DataFrame with coordinates to a new Excel file
df.to_excel('Lägenheter_med_koordinater.xlsx', index=False)
print("Coordinates added and saved to 'koordinater_with_coords.xlsx'")
