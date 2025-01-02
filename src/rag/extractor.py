import sqlite3
import fitz
import tempfile



def extract_pdf_from_db(file_name, section):
    """
    Retrieve and process PDF content from the database, save it as a temporary file.
    Args:
        file_name (str): Name of the PDF file in the database.
        section (str): Section/table where the file is stored.
    Returns:
        Tuple[str, str]: Path to the saved temporary text file and its content.
    """
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT file_content FROM {section} WHERE file_name = ?", (file_name,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"File '{file_name}' not found in section '{section}'.")

        file_content = result[0]
        print(file_content)
        text_content = []
        with fitz.open(stream=file_content, filetype="pdf") as pdf:
            for page in pdf:
                text_content.append(page.get_text())

        # Save extracted text to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", prefix=file_name, mode="w", encoding="utf-8")
        file_content_str = "\n".join(text_content)
        temp_file.write(file_content_str)
        temp_file.close()

        return temp_file.name, file_content_str  # Return the file path and content
    except Exception as e:
        print(f"Error extracting PDF content: {e}")
        raise
    finally:
        conn.close()