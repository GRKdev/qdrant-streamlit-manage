import os
import logging
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredFileLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.schema import Document
import uuid
import streamlit as st


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

qdrant_url = st.secrets.get("QDRANT_URL", os.getenv("QDRANT_URL"))


def save_uploaded_file(uploaded_file):
    try:
        temp_folder = "temp_uploaded_files"
        os.makedirs(temp_folder, exist_ok=True)
        file_path = os.path.join(temp_folder, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        logging.error(f"Error saving the uploaded file: {e}")
        return None


def load_document(file_path):
    try:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".md"):
            loader = UnstructuredMarkdownLoader(
                file_path, encoding="utf-8", mode="elements"
            )
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            loader = UnstructuredFileLoader(file_path, encoding="utf-8")

        loaded_doc = loader.load()
        if hasattr(loaded_doc, "page_content"):
            return loaded_doc.page_content
        else:
            return loaded_doc
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None


def upload_to_vector(file_path, metadata_info, selected_collection_name):
    document_contents = load_document(file_path)
    if document_contents is not None:
        try:
            doc_id = str(uuid.uuid4())

            combined_content = " ".join(doc.page_content for doc in document_contents)

            embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

            document = Document(
                page_content=combined_content,
                metadata={
                    "source": os.path.basename(file_path),
                    **metadata_info,
                },
            )

            Qdrant.from_documents(
                [document],
                embeddings,
                url=qdrant_url,
                collection_name=selected_collection_name,
                prefer_grpc=False,
            )
            logging.info(f"Vector DB Successfully Created with Document ID: {doc_id}!")
        except Exception as e:
            logging.error(f"Error uploading the file: {e}")
    else:
        logging.error("Error loading the file.")
