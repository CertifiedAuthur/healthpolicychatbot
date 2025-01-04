import shutil
import tempfile
import traceback
import sqlite3
import os
import gc
from fast_graphrag import GraphRAG
from src.document_processor import DocumentProcessor
from src.rag.extractor import extract_pdf_from_db
from src.rag.helper import generate_example_queries_entities


process_document = DocumentProcessor()


def prepare_working_dir():
    """
    Prepare a clean temporary working directory for GraphRAG.
    """
    temp_dir = tempfile.mkdtemp()
    shutil.rmtree(temp_dir, ignore_errors=True)  # Clear any existing contents
    temp_dir = tempfile.mkdtemp()  # Recreate a fresh temporary directory
    return temp_dir

def filter_numeric_directories(working_dir):
    """
    Ensure only numeric directories are present in the working directory.
    """
    for subdir in tempfile.TemporaryDirectory()._get_next_temp_name_iterator():
        if not subdir.isdigit():
            shutil.rmtree(subdir)


def clean_working_dir(working_dir):
    """
    Ensure the working directory is clean by recreating it as an empty directory.
    """
    # Recreate the directory by removing and reinitializing it
    shutil.rmtree(working_dir, ignore_errors=True)  # Remove the directory and its contents
    tempfile.mkdtemp(dir=working_dir)  # Recreate the temporary directory

analysis_workspace_path = os.path.join(os.path.abspath(os.getcwd()),"analysis_workspace")

async def process_all_files_in_section(file_name, section, text_content):
    """
    Process all files in the given section by extracting text, creating embeddings,
    and inserting the content into GraphRAG for entity extraction and auto-query generation.
    """
    grag = None
    try:
        example_queries_entities = generate_example_queries_entities(text_content)

        # Initialize GraphRAG with valid working directory
        grag = GraphRAG(
            working_dir= str(analysis_workspace_path),
            domain="Analyze the content to extract key entities, their relationships, and relevant insights.",
            example_queries="\n".join(example_queries_entities["example_queries"]),
            entity_types=example_queries_entities["entity_types"],
        )

        await grag.async_insert(text_content)

        return f"Processed and inserted file '{file_name}' successfully."
            

    except Exception as e:
        print(e)
        return f"Error processing files in section '{section}': {e}"
    finally:
        gc.collect
        
        
def retrieve_all_files_in_section(query, section):
    """
    Process all files in the given section by extracting text, creating embeddings,
    and inserting the content into GraphRAG for entity extraction and auto-query generation.
    """
    
    
    conn = sqlite3.connect("files.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(f"SELECT file_name, file_content FROM {section}")
    files = cursor.fetchall()
    if not files:
        print(f"No files found in section '{section}'.")
        return

    grag = None
    group_response = []
    for file_name, file_content in files:
    
        example_queries_entities = generate_example_queries_entities(file_content)

        # Initialize GraphRAG with valid working directory
        grag = GraphRAG(
            working_dir="./analysis_workspace",
            domain="Analyze the content to extract key entities, their relationships, and relevant insights.",
            example_queries="\n".join(example_queries_entities["example_queries"]),
            entity_types=example_queries_entities["entity_types"],
        )
        response_content = grag.query(query).response
        if response_content != "Sorry, I'm not able to provide an answer to that question.":
        
            group_response.append(response_content)
    
    return "\n".join(group_response)
    
    