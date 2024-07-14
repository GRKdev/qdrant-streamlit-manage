import streamlit as st
from utils.qdrant_operations import (
    get_collections,
    scroll_collection_points,
    delete_point,
)

st.set_page_config(page_title="Retrieve Points", page_icon="🔍")


def search_points(points, search_term):
    if not search_term:
        return points

    search_term = search_term.lower()
    return [
        point
        for point in points
        if search_term in str(point.id).lower()
        or any(search_term in str(value).lower() for value in point.payload.values())
    ]


def retrieve_points():
    st.title("Retrieve, Search, and Delete Points")

    collections = get_collections()
    selected_collection = st.selectbox("Select a Collection", collections)

    if st.button("Retrieve All Points"):
        points = scroll_collection_points(selected_collection)
        st.session_state.points = points
        st.session_state.selected_collection = selected_collection
        st.rerun()

    if "points" in st.session_state:
        search_term = st.text_input("Search points (ID or payload content)")
        filtered_points = search_points(st.session_state.points, search_term)

        st.write(f"Total points retrieved: {len(st.session_state.points)}")
        st.write(f"Points shown after search: {len(filtered_points)}")
        st.write("---")

        for point in filtered_points:
            source_file = point.payload.get("metadata", {}).get("source", "Unknown")
            st.write(f"Source: {source_file}")
            st.write(f"ID: {point.id}")

            with st.expander("View Payload", expanded=False):
                st.json(point.payload)

            if st.button("Delete", key=f"delete_{point.id}"):
                try:
                    delete_point(st.session_state.selected_collection, point.id)
                    st.success(f"Point with ID {point.id} successfully deleted")
                    st.session_state.points = [
                        p for p in st.session_state.points if p.id != point.id
                    ]
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting the point: {str(e)}")

            st.write("---")


if __name__ == "__main__":
    retrieve_points()
