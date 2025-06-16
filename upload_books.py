from pymongo import MongoClient
client = MongoClient("mongodb+srv://22sakthil64:adhavan%4013@cluster0.mongodb.net/?retryWrites=true&w=majority")


db = client["ebooksDB"]
collection = db["books"]

books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "language": "English"},
    {"title": "Ponniyin Selvan", "author": "Kalki", "language": "Tamil"},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez", "language": "Spanish"},
]

collection.insert_many(books)
print("✅ Books inserted successfully.")
