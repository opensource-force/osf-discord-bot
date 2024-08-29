import chromadb
import os

DIRECTORY_CONTAINING_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DB_STORE_PATH = os.path.join(DIRECTORY_CONTAINING_SCRIPT, 'db')
UPLOAD_DIR = os.path.join(DIRECTORY_CONTAINING_SCRIPT, 'uploaded_files')
COLLECTION_NAME = "project_collection"

chroma_client = chromadb.PersistentClient(path=DB_STORE_PATH)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def add_project(name, description, link):
    collection.add(
        documents=[description],
        metadatas=[{"name": name, "link": link}],
        ids=[f"project_{name.replace(' ', '_')}"]
    )

    print(f"Project '{name}' added to the collection.")

def get_project_data(input_text, threshold=0.5):
    query_results = collection.query(
        query_texts=[input_text],
        n_results=5,
        include=['metadatas', 'documents', 'distances']
    )
    
    formatted_results = []
    for doc, metadata, distance in zip(query_results['documents'][0], query_results['metadatas'][0], query_results['distances'][0]):
        if distance > threshold:
            continue  

        name = metadata['name'].replace('name=', '').strip()
        description = doc.replace('description=', '').strip()
        link = metadata['link'].replace('link=', '').strip()
        
        formatted_result = (
            f"**Project Found!** (Match quality: {1 - distance:.2f})\n"
            f"**Name:** {name}\n"
            f"**Description:** {description}\n"
            f"**Link:** {link}\n"
            "This project matches your search criteria. We hope it provides valuable information for your needs."
        )
        formatted_results.append(formatted_result)
    
    if not formatted_results:
        return ["No good matches found for your query. Try broadening your search terms."]
    
    return formatted_results
