import streamlit as st
import sqlite3
import os

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS texts (id INTEGER PRIMARY KEY, content TEXT)")
conn.commit()

menu = ["Files", "Code/Text"]
st.sidebar.title("Welcome to my server! 😎")

choice = st.sidebar.radio("Go to", menu, index=menu.index("Files"))

if choice == "Files":
    st.title("🗂️ File Manager")

    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    files = os.listdir(UPLOAD_FOLDER)
    if files:
        st.subheader("📂 Available Files")
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            with open(file_path, "rb") as f:
                st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)
    else:
        st.info("No files uploaded yet.")

elif choice == "Code/Text":
    st.title("🧑🏻‍💻 Text Saver")

    text_input = st.text_area("Enter your text:")
    if st.button("Save Text"):
        if text_input.strip():
            c.execute("INSERT INTO texts (content) VALUES (?)", (text_input,))
            conn.commit()
            st.success("✅ Text saved successfully!")

    c.execute("SELECT * FROM texts")
    saved_texts = c.fetchall()
    if saved_texts:
        st.subheader("📜 Saved Texts")
        for i, (id, text) in enumerate(saved_texts):
            st.text_area(f"Text {i+1}", text, height=100, disabled=True)
    else:
        st.info("No saved texts yet.")

conn.close()
