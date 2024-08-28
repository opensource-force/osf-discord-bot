import chromadb
import os 

# Define directory paths
DIRECTORY_CONTAINING_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DB_STORE_PATH = os.path.join(DIRECTORY_CONTAINING_SCRIPT, 'db')
UPLOAD_DIR = os.path.join(DIRECTORY_CONTAINING_SCRIPT, 'uploaded_files')

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=DB_STORE_PATH)
COLLECTION_NAME = "project_collection"

def get_or_create_collection(name):
    try:
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
        print(f"Collection '{name}' retrieved successfully.")
    except chromadb.CollectionNotFound:
        collection = chroma_client.create_collection(name=COLLECTION_NAME)
        print(f"Collection '{name}' created successfully.")
    return collection 

def get_context(input_text):
    """
    Retrieve context using ChromaDB.
    """
    query_results = collection.query(
        query_texts=[input_text],
        n_results=5
    )
    return query_results['documents']

