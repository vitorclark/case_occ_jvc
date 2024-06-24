import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def filter_cancer_patients(df):
    df_cancer = df[df['Código do CID'].str.startswith('C', na=False)]
    df_cancer['Tipo de Câncer'] = df_cancer['Código do CID'].str[:3]
    return df_cancer

def get_top_cancer_types(df_cancer, top_n=5):
    cancer_counts = df_cancer['Tipo de Câncer'].value_counts()
    top_5_cancer_types = cancer_counts.head(top_n).index.tolist()
    print("Os 5 tipos de câncer mais comuns são:")
    print(top_5_cancer_types)
    return top_5_cancer_types

def filter_top_cancer_patients(df_cancer, top_cancer_types):
    return df_cancer[df_cancer['Tipo de Câncer'].isin(top_cancer_types)]

def filter_original_df(df, user_ids):
    return df[df['cod_usuario'].isin(user_ids)]

def save_filtered_data(df_interesse, output_path):
    df_interesse.to_csv(output_path, index=False, sep="|")
    print(f"Arquivo {output_path} criado com sucesso!")

def main():
    # Ler o arquivo combinado
    df = load_data('data/combined_data.csv')

    # Filtrar os registros com "Código do CID" que começam com 'C'
    df_cancer = filter_cancer_patients(df)

    # Identificar os 5 tipos de câncer mais comuns
    top_5_cancer_types = get_top_cancer_types(df_cancer)

    # Filtrar os pacientes que têm pelo menos um desses tipos de câncer
    df_top_cancers = filter_top_cancer_patients(df_cancer, top_5_cancer_types)

    # Obter uma lista dos "cod_usuario" desses pacientes
    user_ids = df_top_cancers['cod_usuario'].unique()

    # Filtrar todas as linhas desses pacientes no DataFrame original
    df_interesse = filter_original_df(df, user_ids)

    # Salvar os dados filtrados em um arquivo CSV
    save_filtered_data(df_interesse, 'data/populacao_interesse.csv')

if __name__ == "__main__":
    main()


