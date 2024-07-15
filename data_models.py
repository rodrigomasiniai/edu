from pydantic import BaseModel, Field, validator
from typing import List, Optional
from pydantic.types import HttpUrl
from datetime import datetime

class MetadadosCurso(BaseModel):
    codigo_nome: str = Field(..., description="Código e nome da disciplina")
    natureza: str = Field(..., description="Natureza do curso (e.g., Extensão)")
    carga_horaria_semestral: int = Field(..., gt=0, description="Carga horária semestral em horas")
    carga_horaria_semanal: int = Field(..., gt=0, description="Carga horária semanal em horas")
    perfil_docente: str = Field(..., description="Perfil do docente")
    area_tematica: str = Field(..., description="Área temática do curso")
    linha_eixo_extensao_pesquisa: str = Field(..., description="Linha/eixo de extensão e pesquisa")
    competencias: List[str] = Field(..., description="Competências a serem trabalhadas (lista)")
    ementa: List[str] = Field(..., description="Ementa (termos chave, lista)")
    objetivos: List[str] = Field(..., description="Objetivos de aprendizagem (lista)")
    objetivos_sociocomunitarios: List[str] = Field(..., description="Objetivos sociocomunitários (lista)")
    descricao_publico: str = Field(..., description="Descrição do público envolvido")
    justificativa: str = Field(..., description="Justificativa do curso")
    procedimentos_ensino: List[str] = Field(..., description="Procedimentos de ensino-aprendizagem (lista)")
    temas_aprendizagem: List[str] = Field(..., description="Temas de aprendizagem (lista)")
    procedimentos_avaliacao: List[str] = Field(..., description="Procedimentos de avaliação (lista)")
    bibliografia_basica: List[str] = Field(..., description="Bibliografia básica (lista)")
    bibliografia_complementar: List[str] = Field(..., description="Bibliografia complementar (lista)")
    data_inicio: datetime = Field(..., description="Data de início do curso", example="2024-07-16")

class NucleoConceitual(BaseModel):
    titulo: str = Field(..., description="Título do Núcleo Conceitual")
    conteudo: Optional[str] = Field(None, description="Conteúdo textual gerado")
    video_script: Optional[str] = Field(None, description="Roteiro do vídeo gerado")
    teleprompter_text: Optional[str] = Field(None, description="Texto para teleprompter gerado")

class Modulo(BaseModel):
    titulo: str = Field(..., description="Título do Módulo")
    nucleos_conceituais: List[NucleoConceitual] = Field(..., description="Lista de Núcleos Conceituais")

class CursoData(BaseModel):
    metadata: MetadadosCurso = Field(..., description="Metadados do curso")
    modulos: List[Modulo] = Field(..., description="Módulos do curso")
