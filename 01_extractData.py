import pandas as pd
import requests
from io import StringIO
from bs4 import BeautifulSoup

# URL base
BASE_URL = "https://dadosabertos.c3sl.ufpr.br/curitiba/SESPAMedicoUnidadesMunicipaisDeSaude/"

def get_file_list():
    """
    Obtém a lista de arquivos disponíveis na URL base.

    Returns:
        list: Lista de links para os arquivos CSV.
    """
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    file_links = [a['href'] for a in soup.find_all('a') if a['href'].endswith('Sistema_E-Saude_Medicos_-_Base_de_Dados.csv')]
    return file_links

def process_file(file_name):
    """
    Processa um arquivo CSV baixado da URL base.

    Args:
        file_name (str): Nome do arquivo a ser processado.

    Returns:
        DataFrame: DataFrame processado com as colunas adicionais de data.
    """
    url = BASE_URL + file_name
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('latin1')
        df = pd.read_csv(StringIO(content), sep=';', encoding='latin1', on_bad_lines='skip')
        
        # Extrair data do nome do arquivo
        date_str = file_name.split('_')[0]
        df['Data do Relatório'] = pd.to_datetime(date_str, format='%Y-%m-%d')
        df['Mês do Relatório'] = df['Data do Relatório'].dt.month
        df['Ano do Relatório'] = df['Data do Relatório'].dt.year
        return df
    else:
        print(f"Failed to download {file_name}")
        return None

def filter_files_by_date(file_links):
    """
    Filtra a lista de arquivos por data, mantendo apenas os arquivos de 2020 a 2023.

    Args:
        file_links (list): Lista de links para os arquivos CSV.

    Returns:
        list: Lista de links filtrados.
    """
    return [f for f in file_links if any(year in f for year in ['2020', '2021', '2022', '2023'])]

def combine_dataframes(dfs):
    """
    Combina todos os DataFrames em um único DataFrame.

    Args:
        dfs (list): Lista de DataFrames a serem combinados.

    Returns:
        DataFrame: DataFrame combinado.
    """
    return pd.concat(dfs, ignore_index=True)

def main():
    # Obter a lista de arquivos
    file_links = get_file_list()

    # Filtrar arquivos por data
    filtered_files = filter_files_by_date(file_links)

    # Print da lista de arquivos filtrados
    print("Arquivos filtrados para processamento:")
    for file in filtered_files:
        print(file)

    # Processar e combinar todos os arquivos
    dfs = [process_file(file_name) for file_name in filtered_files if process_file(file_name) is not None]

    # Combinar todos os DataFrames em um único
    combined_df = combine_dataframes(dfs)

    # Salvar o DataFrame combinado em um arquivo CSV
    combined_df.to_csv('data/combined_data.csv', index=False)

if __name__ == "__main__":
    main()
