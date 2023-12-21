import streamlit as st
import pandas as pd
import io


server.maxUploadSize=400

# Função para converter todos os arquivos CSV em uma pasta para o formato XLSX
def convert_all_csv_to_xlsx(uploaded_files):
    converted_files = []

    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.csv'):
            separator = ';' if 'MP' in uploaded_file.name else ','

            try:
                # Lendo o arquivo CSV do arquivo carregado
                df = pd.read_csv(uploaded_file, sep=separator)
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(uploaded_file, sep=separator, encoding='ISO-8859-1')
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo {uploaded_file.name} com a codificação 'ISO-8859-1': {e}")
                    continue

            # Convertendo DataFrame para XLSX
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            converted_files.append(output)

    return converted_files

# Interface Streamlit
st.title('Conversor de CSV para XLSX')

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader("Escolha arquivos CSV", accept_multiple_files=True, type='csv')

# Botão para executar a conversão
if st.button('Converter CSV para XLSX') and uploaded_files:
    with st.spinner('Convertendo arquivos. Por favor, aguarde...'):
        converted_files = convert_all_csv_to_xlsx(uploaded_files)

        # Disponibilizando os arquivos convertidos para download
        for i, file in enumerate(converted_files):
            st.download_button(label=f'Baixar XLSX {i+1}', 
                               data=file, 
                               file_name=f'converted_{i+1}.xlsx', 
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    st.success('Conversão concluída com sucesso!')
