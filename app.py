import streamlit as st
from pymongo import MongoClient
import urllib.parse
import os

# Use Streamlit Secrets to store credentials
username = st.secrets["mongodb"]["username"]
password = urllib.parse.quote_plus(st.secrets["mongodb"]["password"])
uri = f"mongodb+srv://{username}:{password}@cluster0.0d7syo5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create Mongo client
client = MongoClient(uri)
db = client['ebooks_db']
collection = db['books']

# Set admin username for deletion control
ADMIN_USERNAME = st.secrets["admin_username"]

# App Title
st.title("📚 E-Books Library")

# Login Input
if "username" not in st.session_state:
    st.session_state["username"] = ""

with st.sidebar:
    st.subheader("🔐 Login")
    st.session_state["username"] = st.text_input("Enter your username")

st.markdown(f"👤 Logged in as: **{st.session_state['username']}**")

# Add Book Form
with st.expander("➕ Add New Book"):
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        language = st.text_input("Language")
        link = st.text_input("Book Link (URL)")
        submit = st.form_submit_button("Add Book")

        if submit:
            if title and author and language and link:
                collection.insert_one({
                    "title": title,
                    "author": author,
                    "language": language,
                    "link": link
                })
                st.success(f"'{title}' has been added!")
                st.toast("Refreshing...")
                st.stop()  # Ends execution; the app will refresh
            else:
                st.error("All fields are required.")

# Search
search_term = st.text_input("🔍 Search by title, author, or language")

if search_term:
    query = {
        "$or": [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"author": {"$regex": search_term, "$options": "i"}},
            {"language": {"$regex": search_term, "$options": "i"}},
        ]
    }

    # Display Books only after search
    books = list(collection.find(query))

    if books:
        st.subheader("📖 Matching Books")
        for book in books:
            book_id = str(book["_id"])
            st.markdown(f"**{book['title']}** by *{book['author']}* ({book['language']})")
            st.write(f"[Open Book]({book['link']})")

            if st.session_state.get("username") == ADMIN_USERNAME:
                if st.button(f"❌ Delete '{book['title']}'", key=book_id):
                    collection.delete_one({"_id": book["_id"]})
                    st.success(f"'{book['title']}' deleted.")
                    st.toast("Refreshing...")
                    st.stop()  # Ends execution; the app will refresh
            else:
                st.info("🔒 Only admins can delete books.")
    else:
        st.info("No books found. Try a different search.")
