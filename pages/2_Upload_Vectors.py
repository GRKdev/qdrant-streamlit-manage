import streamlit as st
from utils.vector_operations import upload_to_vector, save_uploaded_file
from utils.metadata_parser import (
    parse_custom_metadata,
    parse_source_documents,
    parse_news_document,
)
from utils.qdrant_operations import get_collections
from datetime import datetime

st.set_page_config(page_title="Upload Vectors", page_icon="📤")


def upload_vectors():
    st.title("Upload Vectors")

    collections = get_collections()
    selected_collection = st.selectbox("Select a collection", collections)

    uploaded_files = st.file_uploader(
        "Upload files (Vector)",
        accept_multiple_files=True,
        type=["pdf", "docx", "doc", "txt", "md"],
    )

    st.subheader("Custom Metadata")
    custom_metadata_input = st.text_area(
        "Enter custom metadata (one per line, format 'key: value')",
        height=50,
        help="Format: 'key: value' on each line. For multiple values for a key, repeat the key on different lines.",
    )

    st.subheader("Source Documents Metadata")
    source_docs_input = st.text_area(
        "Enter the details of the source documents (one per line, in order: file name, URL, year, month)",
        height=200,
        help="Format: File name, URL, Year, Month. Each on a separate line. Repeat for multiple documents.",
    )

    st.subheader("News Metadata")
    news_docs_input = st.text_area(
        "Enter the details of the news (one per line, in order: title, URL)",
        height=200,
        help="Format: Title, URL. Each on a separate line.",
    )

    if uploaded_files and st.button("Upload to Vector Store"):
        for uploaded_file in uploaded_files:
            try:
                file_path = save_uploaded_file(uploaded_file)
                custom_metadata = parse_custom_metadata(custom_metadata_input)
                source_documents = parse_source_documents(source_docs_input)
                news_documents = parse_news_document(news_docs_input)

                metadata_info = {
                    "date": custom_metadata.get(
                        "date", int(datetime.now().timestamp())
                    ),
                    "source_documents": source_documents,
                    "source_news": news_documents,
                    **custom_metadata,
                }

                upload_to_vector(file_path, metadata_info, selected_collection)
                st.success(f"Upload successful for {uploaded_file.name}!")
            except Exception as e:
                st.error(f"Error uploading file {uploaded_file.name}: {e}")


if __name__ == "__main__":
    upload_vectors()
