import streamlit as st
from pymongo import MongoClient
import urllib.parse

# Load credentials from secrets
username = st.secrets["mongodb"]["username"]
password = urllib.parse.quote_plus(st.secrets["mongodb"]["password"])
uri = f"mongodb+srv://{username}:{password}@cluster0.0d7syo5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client['ebooks_db']
collection = db['books']

# Admin credentials
ADMIN_USERNAME = st.secrets["admin_username"]
ADMIN_PASSWORD = st.secrets["admin_password"]

# Session variables
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Sidebar Login
with st.sidebar:
    st.subheader("🔐 Login")
    input_username = st.text_input("Username")
    input_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if input_username == ADMIN_USERNAME and input_password == ADMIN_PASSWORD:
            st.session_state["username"] = input_username
            st.session_state["authenticated"] = True
            st.success("Logged in as admin ✅")
        else:
            st.session_state["username"] = input_username
            st.session_state["authenticated"] = False
            st.warning("Logged in as guest (limited access)")

st.title("📚 E-Books Library")
st.markdown(f"👤 Logged in as: **{st.session_state['username']}**")

# Add Book
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
                st.stop()
            else:
                st.error("All fields are required.")

# Search Books
search_term = st.text_input("🔍 Search by title, author, or language")

if search_term:
    query = {
        "$or": [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"author": {"$regex": search_term, "$options": "i"}},
            {"language": {"$regex": search_term, "$options": "i"}},
        ]
    }

    books = list(collection.find(query))

    if books:
        st.subheader("📖 Matching Books")
        for book in books:
            book_id = str(book["_id"])
            st.markdown(f"**{book['title']}** by *{book['author']}* ({book['language']})")
            st.write(f"[Open Book]({book['link']})")

            if st.session_state["authenticated"]:
                if st.button(f"❌ Delete '{book['title']}'", key=book_id):
                    collection.delete_one({"_id": book["_id"]})
                    st.success(f"'{book['title']}' deleted.")
                    st.toast("Refreshing...")
                    st.stop()
            else:
                st.info("🔒 Only admins can delete books.")
    else:
        st.info("No books found. Try a different search.")

