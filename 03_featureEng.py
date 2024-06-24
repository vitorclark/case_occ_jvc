import pandas as pd
import unidecode

def preprocessar_dados(df):
    # Converter "Data do Atendimento" e "Data de Nascimento" para o formato de data
    df['Data do Atendimento'] = pd.to_datetime(df['Data do Atendimento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Criar a coluna 'idade_na_data' que calcula a idade na data do atendimento
    df['idade_na_data'] = df.apply(lambda row: row['Data do Atendimento'].year - row['Data de Nascimento'].year - ((row['Data do Atendimento'].month, row['Data do Atendimento'].day) < (row['Data de Nascimento'].month, row['Data de Nascimento'].day)), axis=1)
    
    return df

def criar_chave_unica(df):
    # Criar a coluna para a data do atendimento no formato desejado
    df['data_formatada'] = df['Data do Atendimento'].dt.strftime('%Y%m%d')
    
    # Criar a chave única concatenando a data formatada, o código do procedimento e o código do usuário
    df['chave_unica'] = df['data_formatada'].astype(str) + '_' + df['Código do Procedimento'].astype(str) + '_' + df['cod_usuario'].astype(str)+ '_' + df['Código do CID'].astype(str)
    
    # Remover duplicatas com base na chave única
    df = df.drop_duplicates(subset='chave_unica')
    
    return df

def adicionar_colunas_consulta(df):
    # Ordenar o DataFrame por cod_usuario e Data do Atendimento
    df = df.sort_values(by=['cod_usuario', 'Data do Atendimento'])
    
    # Adicionar a coluna n_consultas
    df['n_consultas'] = df.groupby('cod_usuario').cumcount() + 1
    
    # Adicionar a coluna ultima_consulta
    df['ultima_consulta'] = df.groupby('cod_usuario')['Data do Atendimento'].shift(1)
    df['ultima_consulta'].fillna(df['Data do Atendimento'], inplace=True)
    
    # Adicionar a coluna cid_ultima_consulta
    df['cid_ultima_consulta'] = df.groupby('cod_usuario')['Código do CID'].shift(1)
    df['cid_ultima_consulta'].fillna(0, inplace=True)
    
    # Adicionar a coluna delta_n_consultas
    df['delta_n_consultas'] = (df['Data do Atendimento'] - df['ultima_consulta']).dt.days
    df['delta_n_consultas'] = df['delta_n_consultas'].astype(int)
    
    # Corrigir o delta_n_consultas para casos onde é zero e não é a primeira consulta
    df.loc[(df['delta_n_consultas'] == 0) & (df['n_consultas'] != 1), 'delta_n_consultas'] = df['delta_n_consultas'].shift(1)
    
    # Substituir valores errados na primeira consulta
    df.loc[df['n_consultas'] == 1, 'ultima_consulta'] = df['Data do Atendimento']
    df.loc[df['n_consultas'] == 1, 'cid_ultima_consulta'] = 0
    df.loc[df['n_consultas'] == 1, 'delta_n_consultas'] = 0
    
    return df

def adicionar_colunas_cancer(df):
    # Adicionar coluna codigo_cid_pai
    df['codigo_cid_pai'] = df['Código do CID'].str.slice(0, 3)
    
    # Total de consultas por cod_usuario
    df['total_consultas'] = df.groupby('cod_usuario')['cod_usuario'].transform('count')
    
    # Primeira consulta com CID de câncer
    df_cancer = df[df['codigo_cid_pai'].str.startswith('C', na=False)]
    primeira_consulta_cancer = df_cancer.groupby('cod_usuario').first().reset_index()
    
    # Remover duplicatas antes do merge
    primeira_consulta_cancer = primeira_consulta_cancer.drop_duplicates(subset='cod_usuario')
    
    df = df.merge(primeira_consulta_cancer[['cod_usuario', 'Data do Atendimento', 'n_consultas', 'Código do CID', 'codigo_cid_pai']], on='cod_usuario', how='left', suffixes=('', '_primeiro_cancer'))
    
    # Renomear colunas para clareza
    df.rename(columns={
        'Data do Atendimento_primeiro_cancer': 'data_primeiro_cancer',
        'n_consultas_primeiro_cancer': 'numero_primeiro_cancer',
        'Código do CID_primeiro_cancer': 'primeiro_cid_cancer',
        'codigo_cid_pai_primeiro_cancer': 'primeiro_cid_pai_cancer'
    }, inplace=True)
    
    # Contagem de CIDs de câncer diferentes por usuário
    df['quantidade_cid_cancer'] = df.groupby('cod_usuario')['Código do CID'].transform(lambda x: x[x.fillna('').str.startswith('C')].nunique())
    
    # Contagem de CIDs diferentes por usuário
    df['quantidade_cid_diferentes'] = df.groupby('cod_usuario')['Código do CID'].transform('nunique')
    
    # Tempo até o primeiro CID de câncer a partir da primeira consulta
    df['primeira_consulta'] = df.groupby('cod_usuario')['Data do Atendimento'].transform('min')
    df['espaco_amostral_antes_diagnostico'] = (df['data_primeiro_cancer'] - df['primeira_consulta']).dt.days
    
    # Calcular espaco_amostral_depois_diagnostico como a diferença entre data_primeiro_cancer e a última consulta do usuário
    ultima_consulta = df.groupby('cod_usuario')['Data do Atendimento'].transform('max')
    df['espaco_amostral_depois_diagnostico'] = (ultima_consulta - df['data_primeiro_cancer']).dt.days
    
    # Substituir NaNs resultantes da ausência de câncer
    df.fillna({
        'data_primeiro_cancer': 0,
        'numero_primeiro_cancer': 0,
        'primeiro_cid_cancer': 0,
        'primeiro_cid_pai_cancer': 0,
        'quantidade_cid_cancer': 0,
        'espaco_amostral_antes_diagnostico': 0,
        'espaco_amostral_depois_diagnostico': 0
    }, inplace=True)
    
    return df

def main():
    # Ler o arquivo combinado
    df = pd.read_csv("data/populacao_interesse.csv", sep='|')
    
    # Preprocessamento dos dados
    df = preprocessar_dados(df)
    
    # Criar chave única
    df = criar_chave_unica(df)
    
    # Adicionar colunas de consulta
    df = adicionar_colunas_consulta(df)
    
    # Adicionar colunas relacionadas a câncer
    df = adicionar_colunas_cancer(df)
    
    # Renomear colunas para minúsculas, sem acentos e com underscores
    df.columns = [unidecode.unidecode(col).lower().replace(' ', '_') for col in df.columns]
    
    df.to_csv('data/base_dados_enrriquecida.csv', index=False)
    
    df = df[
        ['data_do_atendimento', 'data_de_nascimento', 'sexo', 'codigo_da_unidade',
         'codigo_do_cid', 'descricao_do_cid', 'desencadeou_internamento',
         'cod_usuario', 'cod_profissional', 'data_do_relatorio', 'mes_do_relatorio',
         'ano_do_relatorio', 'codigo_cid_pai', 'idade_na_data', 'data_formatada',
         'chave_unica', 'n_consultas', 'ultima_consulta', 'cid_ultima_consulta',
         'delta_n_consultas', 'total_consultas', 'data_primeiro_cancer',
         'numero_primeiro_cancer', 'primeiro_cid_cancer',
         'primeiro_cid_pai_cancer', 'quantidade_cid_cancer',
         'quantidade_cid_diferentes', 'primeira_consulta',
         'espaco_amostral_antes_diagnostico', 'espaco_amostral_depois_diagnostico']
    ]
    
    df.to_csv('data/base_analitica.csv', index=False)

if __name__ == "__main__":
    main()