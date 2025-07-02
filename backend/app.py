from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymongo


# Define path to the frontend/templates directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../frontend/templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app) # Enable CORS for all routes

# MongoDB Atlas connection
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI, tls=True)
db = client.test
collection = db['To-do-page']
    

@app.route("/", methods=["GET"])
def serve_todo_page():
    return render_template("index.html")  # make sure index.html is in the same directory

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        data = request.get_json()
        print("Received data:", data)

        item_name = data.get("itemName")
        item_id = data.get("itemId")
        item_uuid = data.get("itemUUID")
        item_hash = data.get("itemHash")
        item_description = data.get("itemDescription")

        if not all([item_name, item_id, item_uuid, item_hash, item_description]):
            return jsonify({"error": "Missing one or more required fields"}), 400

        todo_item = {
            "itemName": item_name,
            "itemId": item_id,
            "itemUUID": item_uuid,
            "itemHash": item_hash,
            "itemDescription": item_description
        }

        #insert the todo item into the MongoDB collection
        collection.insert_one(todo_item)
        print(" Inserted into MongoDB:", todo_item)
        return jsonify({"message": "Item saved successfully!"}), 200
    
    except Exception as e:
        import traceback
        print("Server Error:", str(e))
        traceback.print_exc()  #this prints full stack trace
        return jsonify({"error": "Server error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
