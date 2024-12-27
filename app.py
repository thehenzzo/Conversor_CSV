import streamlit as st
import os
import re
import csv
from io import StringIO

# Pastas de upload e processamento
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Função para processar o arquivo
def process_list(file_content):
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    lines = file_content.strip().split("\n")
    phone_pattern = re.compile(r"^\+?\d{9,15}$")

    for line in lines:
        items = line.split()
        phone = None
        name = []

        for item in items:
            if phone_pattern.match(item) or item.isdigit():
                phone = f"55{item.strip('+')}"
            else:
                name.append(item)

        if phone:
            csv_writer.writerow([phone, " ".join(name)])

    csv_output.seek(0)
    return csv_output

# Interface principal do Streamlit
st.title("Conversor de Lista para Mailing")
st.write("Faça upload de um arquivo de texto para processar.")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt"])

if uploaded_file:
    st.write(f"Arquivo carregado: {uploaded_file.name}")
    
    # Lê o conteúdo do arquivo
    file_content = uploaded_file.getvalue().decode("utf-8")
    
    # Processa o conteúdo do arquivo
    processed_content = process_list(file_content)
    
    # Salva o arquivo processado
    processed_path = os.path.join(PROCESSED_FOLDER, "mailing.csv")
    with open(processed_path, "w", newline='') as processed_file:
        processed_file.write(processed_content.getvalue())
    
    # Disponibiliza o download do arquivo processado
    st.success("Processamento concluído!")
    st.download_button(
        label="Baixar arquivo processado",
        data=processed_content.getvalue(),
        file_name="mailing.csv",
        mime="text/csv",
    )
