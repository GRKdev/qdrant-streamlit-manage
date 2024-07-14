# Stremlit Qdrant Vector Management

## Overview

Qdrant Vector Management is a Streamlit-based web application designed to simplify the process of managing your Qdrant vector database. This tool provides an intuitive interface for retrieving, searching, and deleting points from your Qdrant collections.


## Features

- **Manage Collections**:
  - View all collections in a database
  - Create new collections
  - Delete collections

- **Retrieve and Search**:
  - View all points in a collection
  - Search points by ID or payload content
  - Display source file information
  - Delete selected points

- **Upload to Vector Database**:
    - Upload vectors from files
    - Add custom metadata
    - Add source document information
    - Add news metadata

## Installation

1. Clone the repository:
    
    ```bash
    git clone
    cd 
    ```
2. Create a virtual environment (optional but recommended):
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the required packages:
    
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the environment variables:
    
    ```bash
    QDRANT_URL="http://localhost:6333"
    ```
5. Run the Streamlit app:
    
    ```bash
    streamlit run Qdrant_app.py
    ```