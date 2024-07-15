######## Imports & Initializations #########
from data_models import CursoData, Modulo, NucleoConceitual
# Importing data models representing the course data structure.

from content_generation import (
    generate_content_for_nucleo_conceitual,
    generate_video_script,
    generate_teleprompter_text
)
# Importing functions for generating educational content, video scripts, and teleprompter text.

import asyncio
# Importing the asyncio module for writing asynchronous programs.

import json 
# Importing the json module for reading and writing JSON data.

####### process_and_generate_content Function #######
async def process_and_generate_content(course_data: CursoData, generator):
    """
    Processes course data to generate content for each conceptual nucleus using the provided generator.
    Args:
        course_data (CursoData): The course data containing metadata and modules.
        generator: The text generation model or function.
    """
    for modulo in course_data.modulos:
        for nucleo_conceitual in modulo.nucleos_conceituais:
            # Generating educational content for each conceptual nucleus.
            nucleo_conceitual.conteudo = await generate_content_for_nucleo_conceitual(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
            # Generating a video script for each conceptual nucleus.
            nucleo_conceitual.video_script = await generate_video_script(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
            nucleo_conceitual.teleprompter_text = await generate_teleprompter_text(
                generator, course_data.metadata, modulo, nucleo_conceitual
            )
    
    # TODO: add logic to store the generated course_data
    # Define how to save it to a database and return it in a specific format.
    print("Course data processed and generated:")
    print(course_data)

###### store_course_data, get_course_data & store_course_feedback Functions #######
async def store_course_data(course_data: CursoData):
    """
    Stores the course data in a JSON file.
    Args:
        course_data (CursoData): The course data to be stored.
    """
    # Storing the course data in a JSON file with UTF-8 encoding and pretty printing (just for now!).
    with open("course_data.json", "w", encoding="utf-8") as f:
        json.dump(course_data.dict(), f, ensure_ascii=False, indent=4)

async def get_course_data():
    """
    Retrieves course data from the JSON file.
    Returns:
        CursoData: The retrieved course data.
    """
    try:
         # Reading the course data from the JSON file and returning it as a CursoData object.
        with open("course_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return CursoData(**data)
    except FileNotFoundError:
        # Returning None if the JSON file is not found.
        return None

async def store_course_feedback(rating: int, comments: str, course_data: CursoData):
    """
    Stores course feedback.
    Args:
        rating (int): The feedback rating.
        comments (str): The feedback comments.
        course_data (CursoData): The course data associated with the feedback.
    """
    # For now, simply print the feedback. Implement database storage as needed.
    print(f"Feedback Received - Rating: {rating}, Comments: {comments}")
    print(f"Course Data: {course_data}")
    # Printing the feedback and associated course data.
