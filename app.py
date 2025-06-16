import streamlit as st
from pymongo import MongoClient
import urllib.parse

# Load credentials from Streamlit secrets
username = st.secrets["mongodb"]["username"]
password = urllib.parse.quote_plus(st.secrets["mongodb"]["password"])  # safely encode special characters
uri = f"mongodb+srv://{username}:{password}@cluster0.0d7syo5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri)
db = client['ebooks_db']
collection = db['books']

# Title
st.title("📚 E-Books Library")

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
                st.experimental_rerun()
            else:
                st.error("All fields are required.")

# Search Field
search_term = st.text_input("🔍 Search by title, author, or language")
query = {}
if search_term:
    query = {
        "$or": [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"author": {"$regex": search_term, "$options": "i"}},
            {"language": {"$regex": search_term, "$options": "i"}},
        ]
    }

# Display Books
books = list(collection.find(query))

if books:
    st.subheader("📖 Matching Books")
    for book in books:
        book_id = str(book["_id"])
        st.markdown(f"**{book['title']}** by *{book['author']}* ({book['language']})")
        st.write(f"[Open Book]({book['link']})")
        if st.button(f"❌ Delete '{book['title']}'", key=book_id):
            collection.delete_one({"_id": book["_id"]})
            st.success(f"'{book['title']}' deleted.")
            st.experimental_rerun()
else:
    st.info("No books found. Try a different search.")
