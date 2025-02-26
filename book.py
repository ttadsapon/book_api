from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Connection URI (replace with your credentials securely)
uri = "mongodb+srv://tudphon:s12345@cluster0.yosw1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)
db = client["book"]
collection = db["books"]

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Create (POST) operation
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    
    new_book = {
        "title": data["title"],
        "author": data["author"],
        "image_url": data["image_url"]
    }

    inserted = collection.insert_one(new_book)
    new_book["_id"] = str(inserted.inserted_id)  
    return jsonify(new_book), 201

# Read (GET) operation - Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(collection.find({}, {"_id": 1, "title": 1, "author": 1, "image_url": 1}))
    for book in books:
        book["_id"] = str(book["_id"])  
    return jsonify({"books": books})

# Read (GET) operation - Get a specific book by ID
@app.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = collection.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])  
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Update (PUT) operation
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    updated = collection.update_one({"_id": ObjectId(book_id)}, {"$set": data})
    
    if updated.matched_count > 0:
        return jsonify({"message": "Book updated successfully"})
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete operation
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    deleted = collection.delete_one({"_id": ObjectId(book_id)})
    
    if deleted.deleted_count > 0:
        return jsonify({"message": "Book deleted successfully"})
    else:
        return jsonify({"error": "Book not found"}), 404

# Check password operation
@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    correct_password = "25846"  

    if password == correct_password:
        return jsonify({"isValid": True})
    else:
        return jsonify({"isValid": False})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)