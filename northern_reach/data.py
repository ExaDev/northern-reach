import pandas as pd
import csv
import numpy as np
import os
import pickle
import mmap

def read_excel(fn):
    # Read the Excel file
    df = pd.read_excel(fn, sheet_name='Tracker', usecols='A:H', header=0)

    # Coalesce the two postcode columns
    df['Postcode'] = df['Postcode of Event'].fillna(df['Postcode of Working Location'])

    # Replace NaN values in each column with "Unknown"
    df['Business Name'] = df['Business Name'].fillna("Unknown")
    df['Industry'] = df['Industry'].fillna("Unknown")
    df['Event Type'] = df['Event Type'].fillna("Unknown")
    df['Date of Event'] = df['Date of Event'].fillna(pd.NaT)  # NaT (Not a Time) for date column
    df['Event Host'] = df['Event Host'].fillna("Unknown")

    # Apply the function to the DataFrame
    df['Latitude'], df['Longitude'] = zip(*df['Postcode'].apply(map_postcode_to_coordinates))

    # Remove rows with None values for latitude or longitude
    df = df.dropna(subset=['Latitude', 'Longitude'])

    return df

def load_postcode_data(file_path):
    pickle_path = file_path.replace('.csv', '.pkl')
    
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return pickle.loads(mm)
    
    postcode_data = {}
    df = pd.read_csv(file_path, usecols=['postcode', 'latitude', 'longitude'])
    df = df.dropna()
    
    postcode_data = dict(zip(df['postcode'], zip(df['latitude'], df['longitude'])))
    
    with open(pickle_path, 'wb') as f:
        pickle.dump(postcode_data, f)
    
    return postcode_data

# Load the data when the module is imported
postcode_data = load_postcode_data('northern_reach/ukpostcodes.csv')

def map_postcode_to_coordinates(postcode):
    cleaned_postcode = postcode.upper()
    return postcode_data.get(cleaned_postcode, (None, None))

