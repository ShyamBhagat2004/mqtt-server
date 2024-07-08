from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB settings
MONGO_URI = "mongodb+srv://shyambhagat:mypassword@cluster0.ltngatr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['lightning_data_db']
collection = db['lightning_strikes']

@app.route('/')
def index():
    data = collection.find().sort("timestamp", -1)  # Fetch data sorted by timestamp
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
