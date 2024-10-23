import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import re

data_frame = pd.DataFrame()
API_KEY = 'AIzaSyA04BO-hlMU_qHr4jR2eIbltbG4-YB8j3c'
def convert_price_to_integer(price):
    # Remove all non-digit characters except for commas
    digits = re.findall(r'\d+', price)
    # Join digits and convert to integer
    return int(''.join(digits)) if digits else 'N/A'

def få_medelinkomst(gata, nummer, ort):
    google_api_link = f'https://maps.googleapis.com/maps/api/geocode/json?address={gata}%20{nummer}%20{ort}&key=AIzaSyA04BO-hlMU_qHr4jR2eIbltbG4-YB8j3c'
    response = requests.get(google_api_link)
    data = response.json()

 
    if 'results' in data and len(data['results']) > 0:
    
 
            
        for component in data['results'][0]['address_components']:
   
            if 'postal_code' in component['types']:
                postnummer = component['long_name'].replace(" ", "")
                print(postnummer)

                link_postinfo = f'https://postnummer.info/{postnummer}/'
                response = requests.get(link_postinfo)

                html = response.text
            
                soup = BeautifulSoup(html, 'html.parser')

                tables = soup.find_all('table')
                target_table = None

                for table in tables:
                    if 'Medellön per månad' in table.get_text():
                        target_table = table
                        break

            
                if target_table:
                    rows = target_table.find('tr')
                    cells = rows.find_all('td')
                    medellön = cells[-1].text.strip()
                    medellön_per_månad = convert_price_to_integer(medellön)
                    lat = data['results'][0]['geometry']['location']['lat']
                    lng = data['results'][0]['geometry']['location']['lng']
                    return [medellön_per_månad, postnummer, lat, lng]
                else: 

                    return ['N/A', postnummer, 'N/A', 'N/A']
        return ['N/A', 'N/A', 'N/A', 'N/A']        
    else:
        return ['N/A', 'N/A', 'N/A', 'N/A']


# Function to convert Living Area and Number of Rooms to floats
def convert_to_float(value):
    # Extract the number before any space or non-numeric characters
    match = re.match(r'^([\d.,]+)', value)
    return float(match.group(1).replace(',', '.')) if match else 'N/A'

# Function to process the dictionary
def process_dict(data_dict):
    # Initialize processed dictionary
    processed_dict = {}
    
    # Iterate through items in the dictionary
    for key, value in data_dict.items():
        if key.lower() in ['slutpris', 'avgift', 'operating cost']:
            if key != 'N/A':
                processed_dict[key] = convert_price_to_integer(value)
        elif key.lower() in ['living area', 'number of rooms', 'additional area', 'outdoor area']:
            if key != 'N/A':
                processed_dict[key] = convert_to_float(value)
        else:
            # Keep other values unchanged
            processed_dict[key] = value
    
    processed_df = pd.DataFrame.from_dict([processed_dict])
    
    return processed_df

def save_to_excel(filename):
    data_frame.to_excel(filename, index=False)

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"
}


def data_from_link(link, css_selector):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.select(css_selector)
    except requests.exceptions.RequestException as e:
        return []

# Function to parse individual sold property data
def parse_sold_property_data(link):
    print(f"Parsing {link}")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh} for URL: {link}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    else:
    
        soup = BeautifulSoup(response.text, 'html.parser')
        sold_price_css = "main div.hcl-flex--container.hcl-flex--justify-space-between.SaleAttributes_sellingPrice__iFujI span.SaleAttributes_sellingPriceText__UZF0W"
        title_css = "main h1.Heading_hclHeading__KufPZ.Heading_hclHeadingSize2__VUGbl"
        area = "main p.Text_hclText__V01MM"

        sold_price_data = soup.select(sold_price_css)

        title_data = soup.select(title_css)


        area_data = soup.select(area)
    


        extracted_data = {}
        extracted_data['titel'] = title_data[0].text.strip()
        extracted_data['slutpris'] = sold_price_data[1].text.strip()


        adress = title_data[0].text.strip()
        last_space_index = adress.rfind(' ')
        gata = adress[:last_space_index]
        nummer = adress[last_space_index + 1:]
        

        sträng = area_data[0].text.strip()
        indexs = sträng.rfind('-')
        indexf = sträng.rfind(',')
        ort = sträng[indexf+2:indexs-1]
        print(ort)
 
        

        medelink = få_medelinkomst(gata, nummer, ort)
        print(medelink[2], medelink[3])
        
        extracted_data['postnummer'] = medelink[1]
        extracted_data['ort'] = ort
        extracted_data['medelinkomst_månad'] = medelink[0]
        extracted_data['latitude'] = medelink[2]
        extracted_data['longitude'] = medelink[3]
        extracted_data['slutpris'] = sold_price_data[1].text.strip()

        
            
        for label, search_text in data_map.items():
            selector = f"p:contains('{search_text}') + div strong"
            element = soup.select_one(selector)
            extracted_data[label] = element.get_text(strip=True) if element else "N/A"
            
        processed_extracted_data = process_dict(extracted_data)
            
        
        global data_frame
        data_frame = pd.concat([data_frame, processed_extracted_data], ignore_index=True)
        time.sleep(random.uniform(0.5,1))
 


data = []
data_map = {
    "Bostadstyp": "Bostadstyp",
    "Upplåtelseform": "Upplåtelseform",
    "Antal rum": "Antal rum",
    "Boarea": "Boarea",
    "Biarea": "Biarea",
    "Uteplats": "Uteplats",
    "Tomtarea":"Tomtarea",
    "Våning": "Våning",
    "Byggår": "Byggår",
    "Driftkostnad": "Driftskostnad",
    "Avgift": "Avgift",
}




# Main loop to scrape multiple pages
def scrape_multiple_pages(start_page, end_page):
    for x in range (1,4):    
        price_max = {
            1:3000000,
            2:3500000,
            3:4000000,


        }
        price_min = {
            1:2500000,
            2:3000000,
            3:3500000,

        }

        for page_number in range(start_page, end_page + 1):
            link = f'https://www.hemnet.se/salda/bostader?sold_age=12m&price_max={price_max[x]}&price_min={price_min[x]}&item_types%5B%5D=bostadsratt&location_ids%5B%5D=17744&by=sale_date&order=asc&page{page_number}'
            print(link)
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            property_links = soup.select("a.hcl-card") 
            if property_links:
                print(f"Found {len(property_links)} property links on {link}.")
            else:
                print(f"No property links found on {link}.")
            i = 0
            for every_link in property_links:
                sold_property_link = "https://www.hemnet.se" + every_link.get("href")
                if i == 0 or i == 1:
                    None
                else:    
                    print(f'hus {i-1}')
                    parse_sold_property_data(sold_property_link)
                i += 1
            save_to_excel('Lägenheter_med_koordinater_komplettering.xlsx') 
            time.sleep(random.uniform(0.5, 1))
    print('Nu är allt klart. Kolla så att det finns en fil till vänste mellan filerna som heter apartment2.xlsx. Om den inte finns ring mig på facetime. Om den finns, stäng ner datorlocket, tryck inte på avknappen utan endast stäng ner skärmen. Håll sedan inne knappen längst till vänster under den stora skärmen tills den släcks. Om den blinkar blått är den inte av. Puss älskar dig ha en bra dag.')
    

# Start scraping pages

scrape_multiple_pages(1, 43)
