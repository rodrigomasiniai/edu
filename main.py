######## Imports & Initializations #########
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Request
# Importing FastAPI and other necessary classes to create a web API, handle file uploads, exceptions, and background tasks.

from fastapi.responses import JSONResponse
# Importing JSONResponse to send JSON responses.

from fastapi.middleware.cors import CORSMiddleware
# Importing CORSMiddleware to handle Cross-Origin Resource Sharing (CORS).

from data_models import CursoData, MetadadosCurso, Modulo, NucleoConceitual
# Importing data models to structure the course data.

from data_extraction import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_course_metadata,
    extract_modulos, 
    validate_course_metadata 
)
# Importing functions for data extraction and validation from various file types.

from content_generation import (
    generate_content_for_nucleo_conceitual,
    generate_video_script,
    generate_teleprompter_text,
    generator
)
# Importing content generation functions for different components of the course.

from utils import process_and_generate_content, store_course_data
# Importing utility functions to process and store course data.

import asyncio
# Importing asyncio for asynchronous programming.

import logging
# Importing logging to log information and errors.

###### App Initialization and CORS Configuration #####
# Initializing the FastAPI application.
app = FastAPI()

# Setting up logging with INFO level to log information and errors.
logging.basicConfig(level=logging.INFO)

# List of allowed origins for CORS.
origins = [
    "http://localhost",  # TODO: Replace with Gradio frontend domain
    "http://localhost:7860",  # The Gradio port
]

# Adding CORS middleware to the FastAPI application to handle requests from 
# specified origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####### Exception Handlers ############
# This function handles ValueError exceptions, returning a JSON response 
# with a 400 status code and the exception message.
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # Exception handler for ValueError exceptions.
    return JSONResponse(
        status_code=400, # Bad Request for validation errors
        content={"message": str(exc)},
    )

# This function handles general exceptions, logging the exception traceback and returning a JSON response 
# with a 500 status code and a generic error message.
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # General exception handler for all other exceptions.
    logging.exception(exc)  # Log the full exception traceback
    return JSONResponse(
        status_code=500, # Internal Server Error for general exceptions
        content={"message": "An internal server error occurred. Please check the logs."},
    )

########### Course Generation Endpoint ##############
@app.post("/generate_course/")
async def generate_course(
    background_tasks: BackgroundTasks,
    form_file: UploadFile = File(...), 
    plan_file: UploadFile = File(...)
):
    """Processes uploaded form and plan files to generate course content."""
    # Endpoint to generate course content from uploaded form and plan files.

    try:
        # Extract text from the uploaded form file.
        form_text = await extract_text_from_file(form_file)
        # Extract text from the uploaded plan file.
        plan_text = await extract_text_from_file(plan_file)    
        # Extract course metadata from the form text.
        course_metadata_dict = extract_course_metadata(form_text)
        # Validate the extracted course metadata.
        validated_metadata = validate_course_metadata(course_metadata_dict)
        # Extract module data from the plan text.
        modulos_data = extract_modulos(plan_text)
        # Create a MetadadosCurso object with the validated metadata.
        course_metadata = MetadadosCurso(**validated_metadata)
        # Create a list of Modulo objects with their respective NucleoConceitual objects.
        modulos = [Modulo(titulo=m['titulo'], nucleos_conceituais=[NucleoConceitual(**nc) for nc in m['nucleos_conceituais']]) for m in modulos_data]
        # Create a CursoData object with the course metadata and modules.
        course_data = CursoData(metadata=course_metadata, modulos=modulos)

        # Store the course data asynchronously for later retrieval
        await store_course_data(course_data) 
        # Add a background task to process and generate content for the course.
        background_tasks.add_task(
            process_and_generate_content, 
            course_data, 
            generator
        )

        # Return a JSON response indicating that the course processing has started.
        return JSONResponse(
            status_code=202, 
            content={"message": "Processamento do curso iniciado. Os resultados serão retornados quando disponíveis."}
        )

    # Raise an HTTPException if an error occurs.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {str(e)}")
        

####### Text Extraction Function ##########
async def extract_text_from_file(file: UploadFile):
    """Extracts text from different file types."""
    # Function to extract text from various file types.

    # Read the contents of the uploaded file.
    contents = await file.read()
    # Get the file extension.
    file_extension = file.filename.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(io.BytesIO(contents)) # Extract text from a PDF file.

    elif file_extension in ["doc", "docx"]:
        return extract_text_from_docx(io.BytesIO(contents)) # Extract text from a DOC or DOCX file.
    
    # Raise an HTTPException if the file type is not supported.
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")
    
