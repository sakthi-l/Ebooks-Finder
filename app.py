from pymongo import MongoClient
import streamlit as st

client = MongoClient("mongodb+srv://22sakthil64:adhavan@13@cluster0.mongodb.net/?retryWrites=true&w=majority")
db = client["ebooksDB"]
collection = db["books"]

st.title("📚 Multilingual eBook Library")

search = st.text_input("🔍 Search by title, author, or language")

if search:
    results = collection.find({
        "$or": [
            {"title": {"$regex": search, "$options": "i"}},
            {"author": {"$regex": search, "$options": "i"}},
            {"language": {"$regex": search, "$options": "i"}}
        ]
    })

    for book in results:
        st.markdown(f"**{book['title']}** by *{book['author']}* ({book['language']})")
