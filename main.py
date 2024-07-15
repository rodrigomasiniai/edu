from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from data_models import CursoData, MetadadosCurso, Modulo, NucleoConceitual
from data_extraction import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_course_metadata,
    extract_modulos, 
    validate_course_metadata 
)
from content_generation import (
    generate_content_for_nucleo_conceitual,
    generate_video_script,
    generate_teleprompter_text,
    generator
)
from utils import process_and_generate_content, store_course_data
import asyncio
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Configure CORS - Allow requests from your Gradio interface domain if needed
origins = [
    "http://localhost",  # Replace with your Gradio frontend domain
    "http://localhost:7860",  # The typical port for Gradio
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400, # Bad Request for validation errors
        content={"message": str(exc)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.exception(exc)  # Log the full exception traceback
    return JSONResponse(
        status_code=500, # Internal Server Error for general exceptions
        content={"message": "An internal server error occurred. Please check the logs."},
    )


@app.post("/generate_course/")
async def generate_course(
    background_tasks: BackgroundTasks,
    form_file: UploadFile = File(...), 
    plan_file: UploadFile = File(...)
):
    """Processes uploaded form and plan files to generate course content."""
    try:
        form_text = await extract_text_from_file(form_file)
        plan_text = await extract_text_from_file(plan_file)

        course_metadata_dict = extract_course_metadata(form_text)
        validated_metadata = validate_course_metadata(course_metadata_dict) # Validate
        
        modulos_data = extract_modulos(plan_text)

        course_metadata = MetadadosCurso(**validated_metadata)
        modulos = [Modulo(titulo=m['titulo'], nucleos_conceituais=[NucleoConceitual(**nc) for nc in m['nucleos_conceituais']]) for m in modulos_data]
        course_data = CursoData(metadata=course_metadata, modulos=modulos)

        # Store the course data for later retrieval
        await store_course_data(course_data)

        background_tasks.add_task(
            process_and_generate_content, 
            course_data, 
            generator
        )

        return JSONResponse(
            status_code=202, 
            content={"message": "Processamento do curso iniciado. Os resultados serão retornados quando disponíveis."}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {str(e)}")

async def extract_text_from_file(file: UploadFile):
    """Extracts text from different file types."""
    contents = await file.read()
    file_extension = file.filename.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(io.BytesIO(contents))
    elif file_extension in ["doc", "docx"]:
        return extract_text_from_docx(io.BytesIO(contents))
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")
