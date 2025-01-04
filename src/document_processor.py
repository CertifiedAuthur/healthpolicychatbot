from io import BytesIO
from src.utils import clean_text
import logging

logging.basicConfig(level=logging.INFO)


class DocumentProcessor:
    SECTION_KEYWORDS = {
        "Request for Proposal (RFP) Document",
        "Terms of Reference (ToR)",
        "Technical Evaluation Criteria",
        "Company and Team Profiles",
        "Environmental and Social Standards",
        "Project History and Relevant Experience",
        "Budget and Financial Documents",
        "Additional Requirements and Compliance Documents"
    }

    def __init__(self):
        pass


    # def process_and_extract(self, input_data):
    #     """
    #     Process input data (plain text, PDFs, or URLs) and extract text.
    #     Args:
    #         input_data: Raw text, file-like object, or URL.
    #     Returns:
    #         Tuple: FAISS vector store and documents list.
    #     """
    #     documents = []

    #     if isinstance(input_data, str):
    #         # If input is a URL, process as a webpage
    #         if input_data.startswith("http"):
    #             webpage_content = self.process_webpage(input_data)
    #             if webpage_content:
    #                 documents = [Document(page_content=webpage_content.strip())]
    #         else:
    #             # Otherwise, treat as plain text
    #             documents = [Document(page_content=input_data.strip())]
    #     elif isinstance(input_data, BytesIO):
    #         # Handle file-like object (PDF)
    #         documents.extend(self.preprocess_document(input_data))
    #         print(f"Documents: {documents}")

    #     # Create FAISS vector store
    #     vectordb = self.create_vectordb(documents)
    #     print(vectordb)
    #     return vectordb, documents
    
    