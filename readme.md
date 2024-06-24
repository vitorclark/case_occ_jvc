
# Case de estudo Grupo Oncoclinicas
**Candidato**: João Vitor Clark
**Data**: 23/06/2024
**Email**:joaovitorclark@gmail.com
## Introdução
O desafio proposto pelo grupo oncoclinicas para  concorrer a vaga de Cientista de Dados  propõe  a criação de uma analise de população de um banco de dados publico com informações de atendimento de consultas medicas da população do sistema pubico de saude de Curitiba . Onde o principal objetivo e identificar a população alvo  e identificar os padrões de uso do mesmo apos um diagnostico de um dos 5 CIDs de cancer mais comum por um paciente

## Itens deste repositorio
01_extractData.py
02_reduce.py
03_featureEng.py
04_analytics.py
requiriments.txt
data (folder)
- base_analitica.csv 
   - gerado pelo script 03_featureEng.py e disponibilizado para  facilitar. Porem caso os scripits sejam executados o arquivo reescrito.

## Acesso ao app.dash 
certifique-se que o arquivo`base_analitica.csv` existe dentro da  pasta data; 

Antes de executar o dashboard, instale as dependências listadas no arquivo `requirements.txt`:

```sh
pip install -r requirements.txt
```

Execute o arquivo 04_analytics.py para iniciar o dashboard:
```sh
python 04_analytics.py
```

Abra o navegador e acesse:

http://127.0.0.1:8050/

## Nota Importante

Durante o processo de limpeza e preparação dos dados, foi identificada a presença de registros duplicados na base de dados. Esses registros possuíam todos os campos exatamente iguais, com exceção da diferença de alguns minutos nos horários de atendimento. 

Para evitar um aumento excessivo e desnecessário de registros, que poderia levar a uma análise cartesiana incorreta e inflacionada, foi adotada a seguinte premissa: **Registros com todas as informações idênticas, exceto pelo horário de atendimento diferenciado por alguns minutos, foram tratados como duplicidades e, portanto, removidos.**

Essa decisão foi baseada na suposição de que essas duplicidades são resultado de erros de input de dados. Consequentemente, apenas um desses registros foi mantido para cada grupo de duplicatas, garantindo que a análise reflita mais precisamente a realidade dos atendimentos realizados.


Durante a análise dos dados, **não foi identificado nenhum campo específico que apontasse claramente os atendimentos de urgência ou emergência**. 

A ausência de um indicador explícito para diferenciar esses tipos de atendimento limita a capacidade de estratificar a análise e obter insights detalhados sobre a utilização dos serviços de saúde em situações de urgência ou emergência.
## Metodologia

Este projeto está dividido em quatro etapas principais, descritas a seguir:

##### Step 1: Extração de Dados

Esta etapa envolve a extração de dados públicos disponíveis no site da Prefeitura de Curitiba. O script `01_extractData.py` baixa e processa os arquivos CSV relacionados ao Sistema E-Saúde, combinando-os em um único DataFrame. Utilizaremos dados dos anos de 2020, 2021, 2022 e 2023 esse grande  DataFrame servirá como a base de dados para as etapas subsequentes.

##### Step 2: Redução de Dados

Nesta etapa, o foco será na seleção da população de interesse (`step2_reduce.py`), que são os pacientes oncológicos dos cinco tipos de câncer mais frequentes na amostra.  para filtrar e reduzir o DataFrame, mantendo apenas as informações relevantes para a análise.

##### Step 3: Engenharia de Variáveis 

A terceira etapa consiste em enriquecer e limpar os dados. O script `03_featureEng.py` será responsável por criar novas variáveis a partir das existentes e garantir que os dados estejam prontos para análise. Esta etapa é crucial para garantir que as análises sejam precisas e informativas.

##### Step 4: Análises (step4_analytics.py)

Na última etapa, `04_analytics.ipynb`, serão realizadas diversas análises estratificadas pelo tipo de câncer. Entre as análises previstas estão a distribuição de sexo e idade da população de interesse, o padrão de utilização do serviço de saúde quanto à distribuição do número de consultas e ao uso do serviço para urgências ou emergências, e a frequência de utilização do serviço ao longo do tempo para os pacientes com o tipo de câncer mais comum.

---

# 01: Data Extraction

## Descrição

Este script, `01_extractData.py`, é responsável por extrair e processar dados de arquivos CSV disponíveis publicamente no site da Prefeitura de Curitiba. Ele baixa os arquivos de dados relacionados ao Sistema E-Saúde e os combina em um único DataFrame. **O processamento pode levar cerca de uma hora** para ser concluído e resulta em um DataFrame com mais de **40 milhões de linhas** considerando o espaço amostral de todos os meses dos anos 2020, 2021, 2022 e 2023.

## Estrutura do Script

### Importações

O script utiliza as seguintes bibliotecas:

- `pandas`: Para manipulação de DataFrames.
- `requests`: Para fazer requisições HTTP e baixar os arquivos CSV.
- `io.StringIO`: Para ler os dados CSV diretamente da resposta HTTP.
- `bs4.BeautifulSoup`: Para analisar o HTML e extrair os links dos arquivos CSV.

### Funções

- **`get_file_list()`**: Obtém a lista de arquivos disponíveis na URL base.
- **`process_file(file_name)`**: Processa um arquivo CSV baixado, adicionando colunas de data baseadas no nome do arquivo.
- **`filter_files_by_date(file_links)`**: Filtra a lista de arquivos para incluir apenas aqueles dos anos 2020 a 2023.
- **`combine_dataframes(dfs)`**: Combina todos os DataFrames em um único DataFrame.
- **`main()`**: Função principal que orquestra a execução das outras funções e salva o DataFrame combinado em um arquivo CSV.

## Schema

O DataFrame resultante tem o seguinte schema e descrição das colunas:

| Coluna                                         | Tipo     | Descrição                                                                 |
|------------------------------------------------|----------|--------------------------------------------------------------------------|
| Data do Atendimento                            | object   | Data em que o atendimento foi realizado.                                 |
| Data de Nascimento                             | object   | Data de nascimento do paciente.                                          |
| Sexo                                           | object   | Sexo do paciente (M/F).                                                  |
| Código do Tipo de Unidade                      | int64    | Código identificador do tipo de unidade de saúde.                        |
| Tipo de Unidade                                | object   | Descrição do tipo de unidade de saúde.                                   |
| Código da Unidade                              | int64    | Código identificador da unidade de saúde.                                |
| Descrição da Unidade                           | object   | Nome ou descrição da unidade de saúde.                                   |
| Código do Procedimento                         | int64    | Código identificador do procedimento realizado.                          |
| Descrição do Procedimento                      | object   | Descrição do procedimento realizado.                                     |
| Código do CBO                                  | int64    | Código Brasileiro de Ocupações do profissional que atendeu o paciente.   |
| Descrição do CBO                               | object   | Descrição da ocupação do profissional que atendeu o paciente.            |
| Código do CID                                  | object   | Código Internacional de Doenças relacionado ao atendimento.              |
| Descrição do CID                               | object   | Descrição da doença ou condição do CID relacionado ao atendimento.       |
| Solicitação de Exames                          | object   | Informações sobre exames solicitados durante o atendimento.              |
| Qtde Prescrita Farmácia Curitibana             | object   | Quantidade de medicamentos prescritos na farmácia curitibana.            |
| Qtde Dispensada Farmácia Curitibana            | int64    | Quantidade de medicamentos dispensados na farmácia curitibana.           |
| Qtde de Medicamento Não Padronizado            | object   | Quantidade de medicamentos não padronizados prescritos.                  |
| Encaminhamento para Atendimento Especialista   | object   | Indica se houve encaminhamento para um especialista.                     |
| Área de Atuação                                | object   | Área de atuação do profissional que realizou o atendimento.              |
| Desencadeou Internamento                       | object   | Indica se o atendimento resultou em internamento.                        |
| Data do Internamento                           | object   | Data do internamento, se aplicável.                                      |
| Estabelecimento Solicitante                    | object   | Nome do estabelecimento que solicitou o internamento.                    |
| Estabelecimento Destino                        | object   | Nome do estabelecimento de destino do internamento.                      |
| CID do Internamento                            | object   | Código do CID relacionado ao internamento.                               |
| Tratamento no Domicílio                        | object   | Informações sobre tratamento no domicílio, se aplicável.                 |
| Abastecimento                                  | object   | Informações sobre o abastecimento no domicílio do paciente.              |
| Energia Elétrica                               | object   | Informações sobre o fornecimento de energia elétrica no domicílio.       |
| Tipo de Habitação                              | object   | Tipo de habitação do paciente.                                           |
| Destino Lixo                                   | object   | Informações sobre o destino do lixo no domicílio do paciente.            |
| Fezes/Urina                                    | object   | Informações sobre o destino de fezes e urina no domicílio do paciente.   |
| Cômodos                                        | float64  | Número de cômodos na habitação do paciente.                              |
| Em Caso de Doença                              | object   | Informações sobre como agir em caso de doença.                           |
| Grupo Comunitário                              | object   | Participação do paciente em grupos comunitários.                         |
| Meio de Comunicação                            | object   | Meios de comunicação disponíveis no domicílio do paciente.               |
| Meio de Transporte                             | object   | Meios de transporte utilizados pelo paciente.                            |
| Município                                      | object   | Município de residência do paciente.                                     |
| Bairro                                         | object   | Bairro de residência do paciente.                                        |
| Nacionalidade                                  | object   | Nacionalidade do paciente.                                               |
| cod_usuario                                    | int64    | Código identificador do usuário (paciente).                              |
| origem_usuario                                 | int64    | Código de origem do usuário.                                             |
| residente                                      | int64    | Indica se o paciente é residente.                                        |
| cod_profissional                               | int64    | Código identificador do profissional que realizou o atendimento.         |

### Execução

Para executar o script, basta rodá-lo no seu ambiente Python:

```sh
python 01_extractData.py
```

---

# 02: Redução de Dados

## Descrição

Este script, `02_reduce.py`, é responsável por filtrar a população de interesse, que são os pacientes oncológicos dos cinco tipos de câncer mais frequentes na amostra. Para filtrar e reduzir o DataFrame, mantendo apenas as informações relevantes para a análise.



## Estrutura do Script

### Importações

O script utiliza as seguintes bibliotecas:

- `pandas`: Para manipulação de DataFrames.

### Funções

- **`load_data(filepath)`**: Carrega o arquivo CSV combinado.
- **`filter_cancer_patients(df)`**: Filtra os registros com "Código do CID" que começam com 'C'.
- **`get_top_cancer_types(df_cancer, top_n=5)`**: Conta a frequência de cada tipo de câncer e identifica os cinco tipos mais comuns.
- **`filter_top_cancer_patients(df_cancer, top_cancer_types)`**: Filtra os pacientes que têm pelo menos um dos tipos de câncer mais comuns.
- **`filter_original_df(df, user_ids)`**: Filtra todas as linhas desses pacientes no DataFrame original.
- **`save_filtered_data(df_interesse, output_path)`**: Salva os dados filtrados em um arquivo CSV.
- **`main()`**: Função principal que orquestra a execução das outras funções e salva o DataFrame combinado em um arquivo CSV.

## Schema

| **Coluna**                                     | **Tipo** | **Descrição**                                                         |
|------------------------------------------------|----------|----------------------------------------------------------------------|
| Data do Atendimento                            | object   | Data em que o atendimento foi realizado.                             |
| Data de Nascimento                             | object   | Data de nascimento do paciente.                                      |
| Sexo                                           | object   | Sexo do paciente (M/F).                                              |
| Código do Tipo de Unidade                      | int64    | Código identificador do tipo de unidade de saúde.                    |
| Tipo de Unidade                                | object   | Descrição do tipo de unidade de saúde.                               |
| Código da Unidade                              | int64    | Código identificador da unidade de saúde.                            |
| Descrição da Unidade                           | object   | Nome ou descrição da unidade de saúde.                               |
| Código do Procedimento                         | int64    | Código identificador do procedimento realizado.                      |
| Descrição do Procedimento                      | object   | Descrição do procedimento realizado.                                 |
| Código do CBO                                  | object   | Código Brasileiro de Ocupações do profissional que atendeu o paciente.|
| Descrição do CBO                               | object   | Descrição da ocupação do profissional que atendeu o paciente.        |
| Código do CID                                  | object   | Código Internacional de Doenças relacionado ao atendimento.          |
| Descrição do CID                               | object   | Descrição da doença ou condição do CID relacionado ao atendimento.   |
| Solicitação de Exames                          | object   | Informações sobre exames solicitados durante o atendimento.          |
| Qtde Prescrita Farmácia Curitibana             | object   | Quantidade de medicamentos prescritos na farmácia curitibana.        |
| Qtde Dispensada Farmácia Curitibana            | int64    | Quantidade de medicamentos dispensados na farmácia curitibana.       |
| Qtde de Medicamento Não Padronizado            | object   | Quantidade de medicamentos não padronizados prescritos.              |
| Encaminhamento para Atendimento Especialista   | object   | Indica se houve encaminhamento para um especialista.                 |
| Área de Atuação                                | object   | Área de atuação do profissional que realizou o atendimento.          |
| Desencadeou Internamento                       | object   | Indica se o atendimento resultou em internamento.                    |
| Data do Internamento                           | object   | Data do internamento, se aplicável.                                  |
| Estabelecimento Solicitante                    | object   | Nome do estabelecimento que solicitou o internamento.                |
| Estabelecimento Destino                        | object   | Nome do estabelecimento de destino do internamento.                  |
| CID do Internamento                            | object   | Código do CID relacionado ao internamento.                           |
| Tratamento no Domicílio                        | object   | Informações sobre tratamento no domicílio, se aplicável.             |
| Abastecimento                                  | object   | Informações sobre o abastecimento no domicílio do paciente.          |
| Energia Elétrica                               | object   | Informações sobre o fornecimento de energia elétrica no domicílio.   |
| Tipo de Habitação                              | object   | Tipo de habitação do paciente.                                       |
| Destino Lixo                                   | object   | Informações sobre o destino do lixo no domicílio do paciente.        |
| Fezes/Urina                                    | object   | Informações sobre o destino de fezes e urina no domicílio do paciente.|
| Cômodos                                        | float64  | Número de cômodos na habitação do paciente.                          |
| Em Caso de Doença                              | object   | Informações sobre como agir em caso de doença.                       |
| Grupo Comunitário                              | object   | Participação do paciente em grupos comunitários.                     |
| Meio de Comunicação                            | object   | Meios de comunicação disponíveis no domicílio do paciente.           |
| Meio de Transporte                             | object   | Meios de transporte utilizados pelo paciente.                        |
| Município                                      | object   | Município de residência do paciente.                                 |
| Bairro                                         | object   | Bairro de residência do paciente.                                    |
| Nacionalidade                                  | object   | Nacionalidade do paciente.                                           |
| cod_usuario                                    | int64    | Código identificador do usuário (paciente).                          |
| origem_usuario                                 | int64    | Código de origem do usuário.                                         |
| residente                                      | int64    | Indica se o paciente é residente.                                    |
| cod_profissional                               | int64    | Código identificador do profissional que realizou o atendimento.     |
| Data do Relatório                              | object   | Data do relatório.                                                   |
| Mês do Relatório                               | int64    | Mês do relatório.                                                    |
| Ano do Relatório                               | int64    | Ano do relatório.                                                    |

### Execução

Para executar o script, basta rodá-lo no seu ambiente Python:

```sh
python step2_reduce.py
```

---

# 03: Feature Engineering e Enriquecimento de Dados

Este script, `step3_featureEng.py`, realiza o pré-processamento e o enriquecimento dos dados, criando novas variáveis e adicionando informações relevantes para análises posteriores.

## Funcionalidades

1. **Preprocessamento de Dados**
   - Conversão das colunas "Data do Atendimento" e "Data de Nascimento" para o formato de data.
   - Cálculo da idade do paciente na data do atendimento e criação da coluna `idade_na_data`.

2. **Criação de Chave Única**
   - Geração de uma chave única para cada atendimento concatenando a data formatada, o código do procedimento e o código do usuário.
   - Remoção de duplicatas com base na chave única.
   - Chabe unica é o concat de `'Data do Atendimento'` + `'Código do Procedimento'` + `'cod_usuario'` + `'Código do CID'`

3. **Adição de Colunas de Consulta**
   - Ordenação dos dados por `cod_usuario` e `Data do Atendimento`.
   - Criação de colunas para o número de consultas (`n_consultas`), data da última consulta (`ultima_consulta`), código do CID da última consulta (`cid_ultima_consulta`), e a diferença de dias entre consultas (`delta_n_consultas`).

4. **Adição de Colunas Relacionadas ao Câncer**
   - Criação da coluna `codigo_cid_pai` para identificar o tipo de câncer.
   - Contagem do total de consultas por usuário (`total_consultas`).
   - Identificação da primeira consulta com diagnóstico de câncer e criação das colunas `data_primeiro_cancer`, `numero_primeiro_cancer`, `primeiro_cid_cancer` e `primeiro_cid_pai_cancer`.
   - Contagem de tipos diferentes de câncer (`quantidade_cid_cancer`) e de CIDs diferentes (`quantidade_cid_diferentes`) por usuário.
   - Cálculo do tempo até o primeiro diagnóstico de câncer e do tempo após o diagnóstico de câncer.

5. **Renomeação de Colunas**
   - As colunas são renomeadas para minúsculas, sem acentos e com underscores para facilitar o manuseio dos dados.

6. **Salvamento dos Dados Enriquecidos**
   - Os dados enriquecidos são salvos nos arquivos `base_dados_enrriquecida.csv` e `base_analitica.csv`.

## Funções

- **`preprocessar_dados(df)`**: Pré-processa os dados convertendo colunas de datas e calculando a idade na data do atendimento.
- **`criar_chave_unica(df)`**: Cria uma chave única para cada atendimento e remove duplicatas com base nesta chave.
- **`adicionar_colunas_consulta(df)`**: Adiciona colunas relacionadas ao número de consultas, última consulta, CID da última consulta e diferença de dias entre consultas.
- **`adicionar_colunas_cancer(df)`**: Adiciona colunas relacionadas ao câncer, como tipo de câncer, contagem de consultas e tempos relacionados ao diagnóstico de câncer.
- **`main()`**: Função principal que executa o pipeline de pré-processamento, criação de chave única, adição de colunas de consulta e câncer, renomeação de colunas e salvamento dos dados enriquecidos.


## Schema

| **Coluna**                                   | **Tipo**  | **Descrição**                                                                 |
|----------------------------------------------|-----------|-------------------------------------------------------------------------------|
| data_do_atendimento                          | object    | Data em que o atendimento foi realizado.                                      |
| data_de_nascimento                           | object    | Data de nascimento do paciente.                                               |
| sexo                                         | object    | Sexo do paciente (M/F).                                                       |
| codigo_da_unidade                            | int64     | Código identificador da unidade de saúde.                                     |
| codigo_do_cid                                | object    | Código Internacional de Doenças relacionado ao atendimento.                   |
| descricao_do_cid                             | object    | Descrição da doença ou condição do CID relacionado ao atendimento.            |
| desencadeou_internamento                     | object    | Indica se o atendimento resultou em internamento.                             |
| cod_usuario                                  | int64     | Código identificador do usuário (paciente).                                   |
| cod_profissional                             | int64     | Código identificador do profissional que realizou o atendimento.              |
| data_do_relatorio                            | object    | Data do relatório.                                                            |
| mes_do_relatorio                             | int64     | Mês do relatório.                                                             |
| ano_do_relatorio                             | int64     | Ano do relatório.                                                             |
| codigo_cid_pai                               | object    | Três primeiros caracteres do código do CID, indicando o tipo de câncer.       |
| idade_na_data                                | int64     | Idade do paciente na data do atendimento.                                     |
| data_formatada                               | int64     | Data do atendimento no formato YYYYMMDD.                                      |
| chave_unica                                  | object    | Chave única para cada atendimento, concatenando data_formatada, código do procedimento e cod_usuario.|
| n_consultas                                  | int64     | Número de consultas do paciente.                                              |
| ultima_consulta                              | object    | Data da última consulta do paciente.                                          |
| cid_ultima_consulta                          | object    | Código do CID da última consulta do paciente.                                 |
| delta_n_consultas                            | int64     | Diferença de dias entre consultas.                                            |
| total_consultas                              | int64     | Total de consultas do paciente.                                               |
| data_primeiro_cancer                         | object    | Data da primeira consulta com diagnóstico de câncer.                          |
| numero_primeiro_cancer                       | float64   | Número da consulta onde ocorreu o primeiro diagnóstico de câncer.             |
| primeiro_cid_cancer                          | object    | Código do CID do primeiro diagnóstico de câncer.                              |
| primeiro_cid_pai_cancer                      | object    | Três primeiros caracteres do código do CID do primeiro diagnóstico de câncer. |
| quantidade_cid_cancer                        | int64     | Quantidade de tipos diferentes de câncer diagnosticados no paciente.          |
| quantidade_cid_diferentes                    | int64     | Quantidade de CIDs diferentes diagnosticados no paciente.                     |
| primeira_consulta                            | object    | Data da primeira consulta do paciente.                                        |
| espaco_amostral_antes_diagnostico            | float64   | Tempo em dias até o primeiro diagnóstico de câncer a partir da primeira consulta.|
| espaco_amostral_depois_diagnostico           | float64   | Tempo em dias desde o primeiro diagnóstico de câncer até a última consulta.   |

## Executando o Script

Para executar o script, use o seguinte comando:

```sh
python step3_featureEng.py
````
---
## 04_analytics.py

### Funções e Análises

#### Análise 1: Distribuição de Sexo e Idade

Essa análise calcula a distribuição por sexo e a média de idade da população de interesse. Os dados são agrupados por `cod_usuario` para evitar duplicidades, e a média de idade é calculada. Em seguida, são gerados gráficos para visualizar essa distribuição, incluindo um gráfico de barras para a distribuição por sexo e um histograma para a distribuição de idade com a linha da média.

#### Análise 2: Distribuição dos CIDs Mais Incidentes Após a Descoberta do Câncer

Essa análise identifica os CIDs mais incidentes após a descoberta do câncer entre os pacientes da população de interesse. Os registros são filtrados para considerar apenas aqueles após o diagnóstico de câncer. A frequência de cada CID é calculada e visualizada em um gráfico de barras mostrando os CIDs mais comuns.

#### Análise 3: Média de Dias Acumulados e Consultas Após Diagnóstico de Câncer

Essa análise calcula a média de dias acumulados após o diagnóstico de câncer, considerando o número de consultas. O tempo é acumulado para cada paciente e a média é calculada por número de consultas. Em seguida, é gerado um gráfico combinado mostrando a quantidade média de dias acumulados e a quantidade de pessoas por número de consultas.

#### Análise 4: Distribuição dos CIDs Mais Comuns por Número de Consultas

Essa análise identifica os CIDs mais comuns por número de consultas, considerando até 8 consultas. Para cada número de consultas, são identificados os 5 CIDs mais comuns e os demais CIDs são agrupados na categoria "Outros CIDs". O gráfico de barras mostra a distribuição dos CIDs mais comuns por número de consultas, com a barra de "Outros CIDs" ajustada proporcionalmente.

#### Análise 5: Tabela de Análise dos CIDs

Essa análise cria uma tabela com a porcentagem de pacientes que tiveram ao menos uma consulta com cada CID, a média de dias para ter a consulta daquele CID e a média do número da consulta com aquele CID. Os dados são agrupados por `cod_usuario` para evitar duplicidades e a tabela é ordenada pela porcentagem de pacientes de forma decrescente.

#### Análise 6: CIDs Mais Procurados Após Diagnóstico

Essa análise identifica os CIDs mais procurados logo após o diagnóstico de câncer, considerando as consultas 2, 3, 4, 5, 6, 7 e 8. São gerados gráficos de barras mostrando os 5 CIDs mais comuns para cada número de consultas, facilitando a visualização dos principais CIDs procurados logo após o diagnóstico.

### Considerações Finais

Essas análises foram realizadas para entender melhor o perfil dos pacientes oncológicos e suas necessidades de atendimento em clínicas de atenção primária. As informações obtidas podem auxiliar no planejamento e organização das novas clínicas para melhor atender essa população específica.
