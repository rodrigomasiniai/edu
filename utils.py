from data_models import CursoData, Modulo, NucleoConceitual
from content_generation import (
    generate_content_for_nucleo_conceitual,
    generate_video_script,
    generate_teleprompter_text
)
import asyncio
import json 

async def process_and_generate_content(course_data: CursoData, generator):
    for modulo in course_data.modulos:
        for nucleo_conceitual in modulo.nucleos_conceituais:
            nucleo_conceitual.conteudo = await generate_content_for_nucleo_conceitual(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
            nucleo_conceitual.video_script = await generate_video_script(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
            nucleo_conceitual.teleprompter_text = await generate_teleprompter_text(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
    
    # Here you can add your logic to store the generated course_data
    # For example, you can save it to a database or return it in a specific format.
    print("Course data processed and generated:")
    print(course_data)

async def store_course_data(course_data: CursoData):
    """Stores the course data in a JSON file (replace with database logic if needed)."""
    with open("course_data.json", "w", encoding="utf-8") as f:
        json.dump(course_data.dict(), f, ensure_ascii=False, indent=4)

async def get_course_data():
    """Retrieves course data from the JSON file (replace with database logic)."""
    try:
        with open("course_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return CursoData(**data)
    except FileNotFoundError:
        return None

async def store_course_feedback(rating: int, comments: str, course_data: CursoData):
    """Stores course feedback (replace with database logic)."""
    # For now, simply print the feedback. Implement database storage as needed.
    print(f"Feedback Received - Rating: {rating}, Comments: {comments}")
    print(f"Course Data: {course_data}")
