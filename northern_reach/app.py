from flask import Flask, render_template
import pandas as pd  # Assuming you're using pandas for your DataFrame
import json
from datetime import datetime

app = Flask(__name__)

# Custom JSON encoder to handle Timestamp objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)

# Load your data
# Replace this with your actual data loading method
df = pd.read_csv('northern_reach/uk_interactions.csv')

@app.route("/")
def map_view():
    # Prepare marker data
    marker_data = []
    for index, row in df.iterrows():
        sectorClass = "".join(row['Sector'].split()).lower().replace('-', '')
        # remove digits from sectorClass
        sectorClass = ''.join([i for i in sectorClass if not i.isdigit()])
        interactionClass = "".join(row['Interaction'].split()).lower().replace('-', '')
        # remove digits from interactionClass
        interactionClass = ''.join([i for i in interactionClass if not i.isdigit()])
        #convert date to string
        interaction_date = row['Date']
        #this is weird for some reason and breaks when refreshing the page
        try:
            date = datetime.strptime(interaction_date, '%Y-%m-%d').strftime('%d %b %y')
        except:
            date = interaction_date
        popup_text = f"""
        <div class="text-content">
        <h2>{row['First Name']} {row['Last Name']} <span>{date}</span></h2>
        <p><a href="mailto:{row['Email']}">{row['Email']}</a></p>
        <p>Postcode: {row['Postcode']}</p>
        </div>
        <div class="pill">
        <span class="leftSide {sectorClass}">{row['Sector']}</span>
        <span class="rightSide {interactionClass}">{row['Interaction']}</span>
        </div>
        """
        marker_data.append({
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'popup': popup_text,
            'date': row['Date'],
            'sector': row['Sector'],
            'interaction': row['Interaction']  # Add this line
        })

    # Convert DataFrame to list of dictionaries, sorted by date in descending order
    df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' is in datetime format
    df_sorted = df.sort_values('Date', ascending=False)
    interactions = df_sorted.to_dict('records')

    # Use the custom JSON encoder to serialize the data
    marker_data_json = json.dumps(marker_data, cls=CustomJSONEncoder)

    # Render the map in the HTML template
    return render_template('app.html', interactions=interactions, marker_data=marker_data_json)

if __name__ == "__main__":
    app.run(debug=True)