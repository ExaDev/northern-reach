from flask import Flask, render_template
import pandas as pd  # Assuming you're using pandas for your DataFrame
import json
from datetime import datetime
import os

from northern_reach.data import read_google_sheet

app = Flask(__name__)

# Custom JSON encoder to handle Timestamp objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)

# Load your data
# Replace this with your actual data loading method
df = read_google_sheet(os.environ.get('GOOGLE_SHEET_ID'))

@app.route("/")
def map_view():
    # Prepare marker data
    marker_data = []
    for index, row in df.iterrows():
        sectorClass = "".join(row['Industry'].split()).lower().replace('-', '')
        sectorClass = ''.join([i for i in sectorClass if not i.isdigit()])
        interactionClass = "".join(row['Event Type'].split()).lower().replace('-', '')
        interactionClass = ''.join([i for i in interactionClass if not i.isdigit()])
        interaction_date = row['Date of Event']
        try:
            date = interaction_date.strftime('%d %b %y')
        except:
            date = str(interaction_date)
        popup_text = f"""
        <div class="text-content">
        <h2>{row['Business Name']} <span>{date}</span></h2>
        <p>Event Host: {row['Event Host']}</p>
        <p>Postcode: {row['Postcode']}</p>
        </div>
        <div class="pill">
        <span class="leftSide {sectorClass}">{row['Industry']}</span>
        <span class="rightSide {interactionClass}">{row['Event Type']}</span>
        </div>
        """
        marker_data.append({
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'popup': popup_text,
            'date': row['Date of Event'],
            'sector': row['Industry'],
            'interaction': row['Event Type']
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
    app.run(debug=True)
