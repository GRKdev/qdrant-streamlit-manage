import streamlit as st

st.set_page_config(
    page_title="Qdrant Vector Management",
    page_icon="IMG/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.title("Welcome to Qdrant Vector Management")
    st.subheader("Efficient Vector Database Management for Your Projects")

    st.write(
        """
    This application provides a user-friendly interface to manage your Qdrant vector database. 
    With our tool, you can easily retrieve, search, and delete points from your collections.
    """
    )

    st.header("Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Manage Collections")
        st.write(
            """
        - Create new collections
        - Delete existing collections
        """
        )

    with col2:
        st.subheader("2. Retrieve and Search")
        st.write(
            """
        - View all points in a collection
        - Search points by ID or payload content
        - Display source file information
        - Delete points as needed
        """
        )

    with col3:
        st.subheader("3. Upload Vectors")
        st.write(
            """
        - Upload vector files (PDF, DOCX, DOC, TXT, MD)
        - Add custom metadata
        - Include source document and news metadata
        """
        )


if __name__ == "__main__":
    main()
