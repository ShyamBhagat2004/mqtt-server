from flask import Flask, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB settings
MONGO_URI = "mongodb+srv://shyambhagat:mypassword@cluster0.ltngatr.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['lightning_data_db']
collection = db['lightning_strikes']

@app.route('/')
def index():
    # Fetch data sorted by timestamp in descending order
    data = collection.find().sort("timestamp", -1)
    # Pass the data to the template for display
    return render_template('index.html', data=data)

if __name__ == '__main__':
    # Fetch the port number from the environment variable PORT, or use 5000 if it's not set
    port = int(os.environ.get('PORT', 5000))
    # Start the Flask app on all available interfaces on the fetched port
    app.run(host='0.0.0.0', port=port, debug=True)
