import io
from typing import BinaryIO
import pytesseract
from PIL import Image
from pdfminer import high_level
from docx import Document
import re
from cerberus import Validator
from datetime import datetime

def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    # Optimize pdfminer for performance (consider different parsing strategies) 
    return high_level.extract_text(pdf_file) 

def extract_text_from_docx(docx_file: BinaryIO) -> str:
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def extract_course_metadata(text: str) -> dict:
    """Extracts course metadata using regex (with table handling)."""
    metadata = {}
    # Example: Extract 'Código e nome da disciplina'
    match = re.search(r'###\s*1\s*Código\s*e\s*nome\s*da\s*disciplina\n(.*?)\n', text, re.IGNORECASE | re.DOTALL)
    if match:
        metadata['codigo_nome'] = match.group(1).strip()
    # Add similar regex patterns for other metadata fields
    return metadata

def extract_modulos(text: str) -> list:
    """Extracts modules and núcleos conceituais."""
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
    """Validates extracted metadata using Cerberus."""
    validator = Validator(course_metadata_schema)
    if validator.validate(metadata):
        return validator.document
    else:
        raise ValueError(f"Metadados do curso inválidos: {validator.errors}")
