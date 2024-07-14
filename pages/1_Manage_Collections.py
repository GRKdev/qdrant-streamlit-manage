import streamlit as st
from utils.qdrant_operations import (
    create_collection,
    delete_collection,
    get_collections,
)
from time import sleep

st.set_page_config(page_title="Manage Collections", page_icon="📊")


def manage_collections():
    st.title("Manage Collections")

    st.header("Create New Collection")
    new_collection_name = st.text_input("Name of the new collection")
    if st.button("Create new collection"):
        if new_collection_name:
            try:
                create_collection(new_collection_name)
                st.success(f"Collection '{new_collection_name}' created successfully!")
                st.session_state.new_collection_created = True
            except Exception as e:
                st.error(f"Error creating the collection: {str(e)}")
        else:
            st.warning("Please enter a name for the collection")

    st.header("Delete Collection")
    collections = get_collections()
    collection_to_delete = st.selectbox("Select a collection to delete", collections)
    if st.button("Delete collection"):
        if collection_to_delete:
            try:
                delete_collection(collection_to_delete)
                st.success(f"Collection '{collection_to_delete}' deleted successfully!")
                st.session_state.collection_deleted = True
            except Exception as e:
                st.error(f"Error deleting the collection: {str(e)}")
        else:
            st.warning("Please select a collection to delete")

    if st.session_state.get("new_collection_created") or st.session_state.get(
        "collection_deleted"
    ):
        sleep(2)
        st.rerun()


if __name__ == "__main__":
    manage_collections()
