######## Imports & Initializations #########
from pydantic import BaseModel, Field, validator, AnyUrl
# Importing Pydantic for data validation and settings management. Field is used to define and describe fields in the model, validator for custom validation logic, and AnyUrl for URL fields.

from typing import List, Optional
# Importing List and Optional from the typing module for type hinting.

from datetime import datetime
# Importing datetime to handle date and time fields.

########## MetadadosCurso Model ##########
# Model to represent the metadata of a course.
class MetadadosCurso(BaseModel):
    # Course code and name. The ellipsis (...) indicates that this field is required.
    codigo_nome: str = Field(..., description="Código e nome da disciplina")
    # Nature of the course, e.g., whether it is an extension course.
    natureza: str = Field(..., description="Natureza do curso (e.g., Extensão)")
    # Semester workload in hours. The gt=0 argument ensures that the value must be greater than 0.
    carga_horaria_semestral: int = Field(..., gt=0, description="Carga horária semestral em horas")
    # Weekly workload in hours. The gt=0 argument ensures that the value must be greater than 0.
    carga_horaria_semanal: int = Field(..., gt=0, description="Carga horária semanal em horas")
    perfil_docente: str = Field(..., description="Perfil do docente")
    # The Theme that is the root of the course.
    area_tematica: str = Field(..., description="Área temática do curso")
    linha_eixo_extensao_pesquisa: str = Field(..., description="Linha/eixo de extensão e pesquisa")
    # List of competencies to be developed.
    competencias: List[str] = Field(..., description="Competências a serem trabalhadas (lista)")
    # List of key terms for the syllabus.
    ementa: List[str] = Field(..., description="Ementa (termos chave, lista)")
    # List of learning objectives
    objetivos: List[str] = Field(..., description="Objetivos de aprendizagem (lista)")
    objetivos_sociocomunitarios: List[str] = Field(..., description="Objetivos sociocomunitários (lista)")
    # Description of the target audience.
    descricao_publico: str = Field(..., description="Descrição do público envolvido")
    justificativa: str = Field(..., description="Justificativa do curso")
    # List of teaching and learning procedures.
    procedimentos_ensino: List[str] = Field(..., description="Procedimentos de ensino-aprendizagem (lista)")
    # List of learning themes.
    temas_aprendizagem: List[str] = Field(..., description="Temas de aprendizagem (lista)")
    # List of evaluation procedures.
    procedimentos_avaliacao: List[str] = Field(..., description="Procedimentos de avaliação (lista)")
    bibliografia_basica: List[str] = Field(..., description="Bibliografia básica (lista)")
    bibliografia_complementar: List[str] = Field(..., description="Bibliografia complementar (lista)")
    data_inicio: datetime = Field(..., description="Data de início do curso", example="2024-07-16")

######## NucleoConceitual Model ###########
# Model to represent a conceptual nucleus within a course module.
class NucleoConceitual(BaseModel):
    # Title of the conceptual nucleus.
    titulo: str = Field(..., description="Título do Núcleo Conceitual")
    # Generated textual content.
    conteudo: str = Field(..., description="Conteúdo textual gerado")
    # Generated video script.
    video_script: str = Field(..., description="Roteiro do vídeo gerado")
    # Optionally generated teleprompter text.
    teleprompter_text: Optional[str] = Field(None, description="Texto para teleprompter gerado")

######### Modulo Model #############
# Model to represent a course module.
class Modulo(BaseModel):
    # Title of the module.
    titulo: str = Field(..., description="Título do Módulo")
    # List of conceptual nuclei within the module.
    nucleos_conceituais: List[NucleoConceitual] = Field(..., description="Lista de Núcleos Conceituais")

####### CursoData Model ##########
 # Model to represent the entire course data, including metadata and modules.
class CursoData(BaseModel):
    # Metadata of the course.
    metadata: MetadadosCurso = Field(..., description="Metadados do curso")
    # List of modules in the course.
    modulos: List[Modulo] = Field(..., description="Módulos do curso")
