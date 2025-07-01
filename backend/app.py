from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymongo


app = Flask(__name__, template_folder="../frontend/templates")
CORS(app)  # Enable CORS for frontend access

# MongoDB Atlas connection
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db['To-do-page']
    

@app.route("/", methods=["GET"])
def serve_todo_page():
    return render_template("index.html")  # make sure index.html is in the same directory

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "Missing itemName or itemDescription"}), 400

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    try:
        collection.insert_one(todo_item)
        return jsonify({"message": "Item saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
