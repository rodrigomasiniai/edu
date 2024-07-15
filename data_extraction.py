######## Imports & Initializations #########
import io
from typing import BinaryIO
# Importing the necessary modules and libraries for handling various file types and validating data.

import pytesseract
from PIL import Image
# Importing Pytesseract and PIL (Pillow) for OCR (Optical Character Recognition) to extract text from images.

from pdfminer import high_level
# Importing pdfminer for extracting text from PDF files.

from docx import Document
# Importing the python-docx library to read DOCX files.

import re
# Importing the regex library for pattern matching and text extraction.

from cerberus import Validator
# Importing Cerberus for validating the extracted metadata against a predefined schema.

from datetime import datetime
# Importing datetime to handle date and time fields.

# Function to extract text from a PDF file.
def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    # Optimize pdfminer for performance (consider different parsing strategies) 
    return high_level.extract_text(pdf_file) 

# Function to extract text from a DOCX file.
def extract_text_from_docx(docx_file: BinaryIO) -> str:
    # Loading the DOCX file using python-docx.
    doc = Document(docx_file)
    # Joining all paragraphs' text into a single string separated by newline characters.
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text from an image file.
def extract_text_from_image(image: Image.Image) -> str:
    # Using Pytesseract to perform OCR and extract text from the provided image.
    return pytesseract.image_to_string(image)

def extract_course_metadata(text: str) -> dict:
    """Extracts course metadata using regex (with table handling).
    text: The text from which metadata is to be extracted.
    Returns: A dictionary containing the extracted metadata.
    """
    metadata = {}
    
    # Example: Extract 'Código e nome da disciplina'
    match = re.search(r'###\s*1\s*Código\s*e\s*nome\s*da\s*disciplina\n(.*?)\n', text, re.IGNORECASE | re.DOTALL)
    if match:
        metadata['codigo_nome'] = match.group(1).strip()
    
    # TODO: Add similar regex patterns for other metadata fields
    # Options?
    
    # Returning the extracted metadata as a dictionary.
    return metadata

def extract_modulos(text: str) -> list:
    """Extracts modules and núcleos conceituais from the provided text.
    text: The text from which modules and conceptual nuclei are to be extracted.
    Returns: A list of dictionaries, each containing the title and conceptual nuclei of a module.
    """
    modulos = []
    
    # Example: Extract modules and their titles
    for modulo_match in re.findall(r'###\s*(\d+)\s*(.*?)\n(.*?)(?=\n###|\Z)', text, re.IGNORECASE | re.DOTALL):
        modulo_titulo = modulo_match[1].strip()
        nucleos_conceituais = []
        
        # Example: Extract núcleos conceituais within each module
        for nucleo_match in re.findall(r'\d+\.\d+\s*(.*?)\n', modulo_match[2], re.IGNORECASE):
            nucleos_conceituais.append({'titulo': nucleo_match.strip()})
        
        modulos.append({'titulo': modulo_titulo, 'nucleos_conceituais': nucleos_conceituais})
    
    return modulos

# Cerberus schema for validation 
course_metadata_schema = {
    'codigo_nome': {'type': 'string', 'required': True},
    'natureza': {'type': 'string', 'required': True, 'allowed': ['Extensão', 'Aperfeiçoamento', 'Outro']},
    'carga_horaria_semestral': {'type': 'integer', 'required': True, 'min': 1},
    'carga_horaria_semanal': {'type': 'integer', 'required': True, 'min': 1},
    'perfil_docente': {'type': 'string', 'required': True},
    'area_tematica': {'type': 'string', 'required': True},
    'linha_eixo_extensao_pesquisa': {'type': 'string', 'required': True},
    'competencias': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'ementa': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'objetivos': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'objetivos_sociocomunitarios': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'descricao_publico': {'type': 'string', 'required': True},
    'justificativa': {'type': 'string', 'required': True},
    'procedimentos_ensino': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'temas_aprendizagem': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'procedimentos_avaliacao': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'bibliografia_basica': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'bibliografia_complementar': {'type': 'list', 'required': True, 'schema': {'type': 'string'}},
    'data_inicio': {'type': 'datetime', 'coerce': 'datetime', 'min': datetime.now(), 'required': True},
}

def validate_course_metadata(metadata: dict) -> dict:
    """Validates extracted metadata using Cerberus.
    metadata: The dictionary containing extracted metadata.
    Returns: The validated metadata.
    Raises:
        ValueError: If the metadata does not conform to the schema.
    """
    # Creating a Cerberus validator with the defined schema.
    validator = Validator(course_metadata_schema)
    # Returning the validated metadata if it conforms to the schema.
    if validator.validate(metadata):
        return validator.document
    else:
        # Raising a ValueError if the metadata does not conform to the schema.
        raise ValueError(f"Metadados do curso inválidos: {validator.errors}")
        

