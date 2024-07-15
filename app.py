import gradio as gr
from main import app as fastapi_app
from fastapi.testclient import TestClient
from data_models import MetadadosCurso
from utils import (
    get_course_data,
    store_course_feedback 
)

client = TestClient(fastapi_app)

def process_course_data(
    codigo_nome, natureza, carga_horaria_semestral,
    carga_horaria_semanal, perfil_docente, area_tematica,
    linha_eixo_extensao_pesquisa, competencias, ementa,
    objetivos, objetivos_sociocomunitarios, descricao_publico,
    justificativa, procedimentos_ensino, temas_aprendizagem,
    procedimentos_avaliacao, bibliografia_basica,
    bibliografia_complementar, form_file, plan_file
):
    try:
        # Validate input data (add more validation as needed)
        if not all([codigo_nome, natureza, carga_horaria_semestral, 
                    carga_horaria_semanal, perfil_docente, area_tematica, 
                    linha_eixo_extensao_pesquisa, competencias, ementa, 
                    objetivos, objetivos_sociocomunitarios, descricao_publico, 
                    justificativa, procedimentos_ensino, temas_aprendizagem, 
                    procedimentos_avaliacao, bibliografia_basica, 
                    bibliografia_complementar, form_file, plan_file]):
            return "Por favor, preencha todos os campos e envie os arquivos."

        with open(form_file.name, "rb") as f:
            form_content = f.read()
        with open(plan_file.name, "rb") as f:
            plan_content = f.read()

        response = client.post(
            "/generate_course/",
            files={
                "form_file": (form_file.name, form_content, form_file.type),
                "plan_file": (plan_file.name, plan_content, plan_file.type),
            },
        )

        if response.status_code == 202:
            return "Curso enviado com sucesso! Aguarde o processamento."
        else:
            return f"Erro ao enviar o curso: {response.text}"

    except Exception as e:
        return f"Erro: {str(e)}"

# -------------------- #
# Improved Interface #
# -------------------- #

iface = gr.Interface(
    fn=process_course_data,
    inputs=[
        gr.Textbox(label="Código e Nome da Disciplina"),
        gr.Dropdown(["Extensão", "Aperfeiçoamento", "Outro"], label="Natureza"),
        gr.Number(label="Carga Horária Semestral (horas)"),
        gr.Number(label="Carga Horária Semanal (horas)"),
        gr.Textbox(label="Perfil Docente"),
        gr.Textbox(label="Área Temática"),
        gr.Textbox(label="Linha Eixo de Extensão e Pesquisa"),
        gr.Textbox(label="Competências (separadas por vírgula)"),
        gr.Textbox(label="Ementa (termos chave, separados por vírgula)"),
        gr.Textbox(label="Objetivos (separados por vírgula)"),
        gr.Textbox(label="Objetivos Sociocomunitários (separados por vírgula)"),
        gr.Textbox(label="Descrição do Público Envolvido"),
        gr.Textbox(label="Justificativa"),
        gr.Textbox(label="Procedimentos de Ensino-Aprendizagem (separados por vírgula)"),
        gr.Textbox(label="Temas de Aprendizagem (separados por vírgula)"),
        gr.Textbox(label="Procedimentos de Avaliação (separadas por vírgula)"),
        gr.Textbox(label="Bibliografia Básica (separadas por vírgula)"),
        gr.Textbox(label="Bibliografia Complementar (separadas por vírgula)"),
        gr.File(label="Formulário (PDF/DOCX)", type=["pdf", "docx"]),
        gr.File(label="Plano de Ensino (PDF/DOCX)", type=["pdf", "docx"]),
    ],
    outputs=[
        gr.Textbox(label="Status")
    ],
    title="Criador de Curso com IA - VantechNenonetics", 
    description="Insira os metadados do seu curso e carregue os arquivos relevantes para gerar conteúdo automaticamente.",
)


with gr.Blocks(
    css=".gr-button { background-color: #A27B5C; color: #DCD7C9 }",  # Improved CSS
    title="Criador de Curso com IA - VantechNenonetics", 
) as demo:

    with gr.Tab("Criar Curso"):
        iface.render()  # Embed the initial course creation interface

    with gr.Tab("Visualizar e Editar"):  # New tab for content preview and editing 
        # You would likely retrieve and display generated course data from storage/database
        course_data_display = gr.JSON(label="Dados do Curso (JSON)")
        with gr.Row():
            with gr.Column():
                original_content = gr.Textbox(
                    label="Conteúdo Original (do arquivo)", 
                    lines=15,
                    interactive=False  
                )
            with gr.Column():
                generated_content = gr.Textbox(
                    label="Conteúdo Gerado pela IA",
                    lines=15,
                    interactive=True # Editable
                )
        feedback = gr.Radio(
            choices=["👍 Gostei", "👎 Não gostei"], 
            label="Feedback"
        )
        submit_feedback_btn = gr.Button("Enviar Feedback")

    # ... (Event handlers for feedback submission, saving edited content)

demo.launch()
