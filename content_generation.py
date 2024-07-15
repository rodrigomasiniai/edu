from transformers import pipeline
import asyncio
from typing import List, Dict
from data_models import MetadadosCurso, Modulo, NucleoConceitual

generator = pipeline('text-generation', model='mistralai/Mistral-7B-Instruct-v0.3')

async def generate_content_for_nucleo_conceitual(
    generator, 
    metadata: MetadadosCurso, 
    modulo: Modulo, 
    nucleo_conceitual: NucleoConceitual
) -> str:
    """Generates educational content for a Nucleo Conceitual."""
    
    prompt = f"""
    ### Gere um conteúdo educacional para um Núcleo Conceitual de um curso universitário.

    **Informações do Curso:**
    * **Nome do Curso:** {metadata.codigo_nome}
    * **Descrição do Público:** {metadata.descricao_publico}
    * **Objetivos de Aprendizagem:** {', '.join(metadata.objetivos)}

    **Informações do Módulo:**
    * **Título do Módulo:** {modulo.titulo}

    **Informações do Núcleo Conceitual:**
    * **Título do Núcleo Conceitual:** {nucleo_conceitual.titulo}

    **Exemplo de Conteúdo:**

    ## Introdução
    Este Núcleo Conceitual aborda... 

    ### Subtópico 1
    * Detalhe 1
    * Detalhe 2 
    * Exemplo: ...

    ## Conclusão
    Em resumo... 

    **Conteúdo Gerado:**

    ## {nucleo_conceitual.titulo}

    (Insira aqui o conteúdo educacional. Siga o exemplo acima.
    Seja conciso, claro e envolvente.) 
    """

    result = generator(
        prompt,
        max_new_tokens=1024,
        num_return_sequences=1,
        temperature=0.7
    )
    return result[0]['generated_text']

async def generate_video_script(
    generator,
    metadata: MetadadosCurso,
    modulo: Modulo,
    nucleo_conceitual: NucleoConceitual
) -> str:
    """Generates a video script for a Nucleo Conceitual."""

    prompt = f"""
    ### Crie um roteiro para um vídeo educacional curto e envolvente.

    **Informações do Curso:**
    * **Nome do Curso:** {metadata.codigo_nome}
    * **Descrição do Público:** {metadata.descricao_publico}
    * **Objetivos de Aprendizagem:** {', '.join(metadata.objetivos)}

    **Informações do Módulo:**
    * **Título do Módulo:** {modulo.titulo}

    **Informações do Núcleo Conceitual:**
    * **Título do Núcleo Conceitual:** {nucleo_conceitual.titulo}

    **Exemplo de Roteiro:**

    ## Introdução (0:00-0:30)
    * **Visual:** Uma animação do título do curso e do módulo.
    * **Narração:** Olá! Bem-vindos ao curso {metadata.codigo_nome}. Neste vídeo, vamos explorar {nucleo_conceitual.titulo}, um tópico fundamental em {modulo.titulo}.

    ## Conceitos-Chave (0:30-3:00)
    * **Visual:** Gráficos e diagramas ilustrando os conceitos-chave.
    * **Narração:** (Explique os conceitos-chave de forma clara e concisa, usando exemplos relevantes para o público-alvo.)

    ## Aplicação Prática (3:00-4:00)
    * **Visual:** Cenas mostrando exemplos práticos da aplicação dos conceitos.
    * **Narração:** (Demonstre como os conceitos aprendidos podem ser aplicados na prática.)

    ## Conclusão (4:00-4:30)
    * **Visual:** Um resumo dos pontos principais abordados no vídeo.
    * **Narração:** (Recapitule os pontos-chave e incentive os alunos a explorar mais o assunto.)

    **Roteiro Gerado:**

    ## {nucleo_conceitual.titulo}

    (Insira aqui o roteiro do vídeo. Siga o exemplo acima.
    Seja criativo e envolvente.)
    """

    result = generator(
        prompt,
        max_new_tokens=512,
        num_return_sequences=1,
        temperature=0.7
    )
    return result[0]['generated_text']

async def generate_teleprompter_text(
    generator,
    metadata: MetadadosCurso,
    modulo: Modulo,
    nucleo_conceitual: NucleoConceitual
) -> str:
    """Generates teleprompter text for a Nucleo Conceitual."""

    # First, generate the content for the Núcleo Conceitual
    content = await generate_content_for_nucleo_conceitual(generator, metadata, modulo, nucleo_conceitual)

    prompt = f"""
    ### Crie um texto para teleprompter para um vídeo educacional.

    **Informações do Curso:**
    * **Nome do Curso:** {metadata.codigo_nome}
    * **Descrição do Público:** {metadata.descricao_publico}

    **Informações do Módulo:**
    * **Título do Módulo:** {modulo.titulo}

    **Informações do Núcleo Conceitual:**
    * **Título do Núcleo Conceitual:** {nucleo_conceitual.titulo}

    **Conteúdo do Núcleo Conceitual:**
    {content}

    **Exemplo de Texto para Teleprompter:**

    Olá a todos! Sejam bem-vindos ao curso {metadata.codigo_nome}. Hoje, vamos mergulhar em {nucleo_conceitual.titulo}, um tópico essencial em {modulo.titulo}. 
    (Continue o texto para teleprompter, adaptando o conteúdo do Núcleo Conceitual. 
    Seja claro, conciso e mantenha um tom amigável e convidativo.)

    **Texto para Teleprompter Gerado:**

    (Insira aqui o texto para teleprompter. Siga o exemplo acima.
    Mantenha um tom natural e fácil de ler em voz alta.)
    """

    result = generator(
        prompt,
        max_new_tokens=1024,
        num_return_sequences=1,
        temperature=0.7
    )
    return result[0]['generated_text']
