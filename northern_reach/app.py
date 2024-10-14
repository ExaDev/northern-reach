from flask import Flask, render_template
import pandas as pd  # Assuming you're using pandas for your DataFrame
import json
from datetime import datetime

from northern_reach.data import read_excel

app = Flask(__name__)

# Custom JSON encoder to handle Timestamp objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)

# # Load your data
# # Replace this with your actual data loading method
# df = pd.read_csv('northern_reach/uk_interactions.csv')

df = read_excel("northern_reach/Northern Reach CRM 2024.xlsx")

@app.route("/")
def map_view():
    # Prepare marker data
    marker_data = []
    for index, row in df.iterrows():
        popup_text = f"""
        <b>Business Name:</b> {row['Business Name']}<br>
        <b>Industry:</b> {row['Industry']}<br>
        <b>Postcode:</b> {row['Postcode']}<br>
        <b>Event Type:</b> {row['Event Type']}<br>
        <b>Date of Event:</b> {row['Date of Event']}<br>
        <b>Event Host:</b> {row['Event Host']}
        """
        marker_data.append({
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'popup': popup_text,
            'date': row['Date of Event'],
            'industry': row['Industry'],
            'event_type': row['Event Type']
        })

    # Convert DataFrame to list of dictionaries, sorted by date in descending order
    df['Date of Event'] = pd.to_datetime(df['Date of Event'])  # Ensure 'Date of Event' is in datetime format
    df_sorted = df.sort_values('Date of Event', ascending=False)
    interactions = df_sorted.to_dict('records')

    # Use the custom JSON encoder to serialize the data
    marker_data_json = json.dumps(marker_data, cls=CustomJSONEncoder)

    # Render the map in the HTML template
    return render_template('app.html', interactions=interactions, marker_data=marker_data_json)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)