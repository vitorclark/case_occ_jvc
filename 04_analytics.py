import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Suas funções de análise e gráficos
def analisar_distribuicao_sexo_idade(populacao_interesse):
    populacao_interesse_grouped = populacao_interesse.groupby('cod_usuario').agg({
        'sexo': 'first',
        'idade_na_data': 'mean'
    }).reset_index()

    sexo_distribution = populacao_interesse_grouped['sexo'].value_counts(normalize=True) * 100
    sexo_counts = populacao_interesse_grouped['sexo'].value_counts()
    mean_age_by_sex = populacao_interesse_grouped.groupby('sexo')['idade_na_data'].mean()

    sexo_stats = pd.DataFrame({
        'sexo': sexo_counts.index,
        'Contagem': sexo_counts.values,
        'Porcentagem': sexo_distribution.values.round(2),
        'Média de Idade': mean_age_by_sex.values.round(2)
    })

    fig1 = px.bar(sexo_stats, x='sexo', y='Contagem', color='sexo', title='Distribuição por Sexo',
                  text='Contagem', color_discrete_sequence=['#17becf', '#2ca02c'])
    fig1.update_layout(template='plotly_white')

    mean_age = populacao_interesse_grouped['idade_na_data'].mean()

    fig2 = px.histogram(populacao_interesse_grouped, x='idade_na_data', nbins=30, title='Distribuição por Idade', color_discrete_sequence=['#66CCCC'])
    fig2.add_shape(
        type='line',
        x0=mean_age,
        y0=0,
        x1=mean_age,
        y1=300,
        line=dict(color='red', width=3, dash='dash'),
        name='Média'
    )
    fig2.update_layout(
        xaxis_title='Média de Idade por Paciente',
        template='plotly_white'
    )
    return fig1, fig2

def analisar_cids(populacao_interesse):
    df = populacao_interesse.groupby(['cod_usuario', 'codigo_do_cid']).first().reset_index()

    cid_analysis = df.groupby('codigo_do_cid').agg(
        Frequência=('codigo_do_cid', 'size'),
        Porcentagem=('cod_usuario', lambda x: x.nunique() / df['cod_usuario'].nunique() * 100),
        Média_dias_para_consulta=('delta_n_consultas', 'mean'),
        Média_numero_de_consultas=('n_consultas', 'mean')
    ).reset_index()

    cid_analysis = cid_analysis.round(2)
    cid_analysis = cid_analysis.sort_values(by="Porcentagem", ascending=False)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(cid_analysis.columns),
                    fill_color='#C8D4E3',
                    align='left'),
        cells=dict(values=[cid_analysis[col] for col in cid_analysis.columns],
                   fill_color='lavender',
                   align='left',
                   font=dict(color='black'))
    )])
    fig.update_layout(title='Análise de CID', template='plotly_white')
    return fig

def grafico_distribuicao_cids(populacao_interesse):
    df_after_cancer = populacao_interesse[populacao_interesse['espaco_amostral_depois_diagnostico'] > 0]
    cid_distribution = df_after_cancer['codigo_cid_pai'].value_counts().reset_index()
    cid_distribution.columns = ['Código CID', 'Frequência']
    fig = px.bar(cid_distribution.head(10), x='Código CID', y='Frequência', title='Distribuição dos CIDs Mais Incidentes Após a Descoberta do Câncer',
                 text='Frequência', color='Código CID', color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(template='plotly_white')
    return fig

def grafico_media_dias_consultas(populacao_interesse):
    df_after_cancer = populacao_interesse[populacao_interesse['espaco_amostral_depois_diagnostico'] > 0]
    df_after_cancer['dias_acumulados'] = df_after_cancer.groupby('cod_usuario')['delta_n_consultas'].cumsum()

    df_after_cancer_grouped = df_after_cancer[df_after_cancer['n_consultas'] <= 40].groupby('n_consultas').agg({
        'dias_acumulados': 'mean',
        'cod_usuario': 'count'
    }).reset_index()

    df_after_cancer_grouped.rename(columns={
        'n_consultas': 'Número de Consultas',
        'dias_acumulados': 'Média de Dias Acumulados Após Diagnóstico',
        'cod_usuario': 'Quantidade de Pessoas'
    }, inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_after_cancer_grouped['Número de Consultas'],
        y=df_after_cancer_grouped['Quantidade de Pessoas'],
        name='Quantidade de Pessoas',
        marker_color='rgba(0, 204, 204, 0.6)',
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=df_after_cancer_grouped['Número de Consultas'],
        y=df_after_cancer_grouped['Média de Dias Acumulados Após Diagnóstico'],
        mode='lines+markers',
        name='Média de Dias Acumulados Após Diagnóstico',
        line=dict(color='rgba(23, 190, 207, 1)', width=2),
        marker=dict(color='rgba(23, 190, 207, 1)', size=8)
    ))

    fig.update_layout(
        title='Média de Dias Acumulados e Consultas Após Diagnóstico de Câncer com Distribuição de Pessoas',
        template='plotly_white',
        yaxis=dict(title='Média de Dias Acumulados Após Diagnóstico'),
        yaxis2=dict(title='Quantidade de Pessoas', overlaying='y', side='right'),
        xaxis=dict(title='Número de Consultas'),
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Ler a base analítica
df = pd.read_csv('data/base_analitica.csv')

# Filtrar a população de interesse
populacao_interesse = df[(df['espaco_amostral_depois_diagnostico'] > 0) & (df['total_consultas'] > 1)]

# Executar as análises e gerar os gráficos
fig1, fig2 = analisar_distribuicao_sexo_idade(populacao_interesse)
fig3 = grafico_distribuicao_cids(populacao_interesse)
fig4 = grafico_media_dias_consultas(populacao_interesse)
fig5 = analisar_cids(populacao_interesse)

# Descrições das análises
descricao_distribuicao_sexo_idade = """
### Distribuição de Sexo e Idade

Esta análise mostra a distribuição de sexo e idade dos pacientes oncológicos que fazem parte da população de interesse. A distribuição por sexo é representada por um gráfico de barras, enquanto a distribuição por idade é apresentada por um histograma com uma linha indicando a média de idade.
"""

descricao_distribuicao_cids = """
### Distribuição dos CIDs Mais Incidentes

Este gráfico de barras exibe a distribuição dos 10 CIDs mais incidentes após a descoberta do câncer, indicando a frequência de cada CID entre os pacientes da população de interesse.
"""

descricao_media_dias_consultas = """
### Média de Dias Acumulados e Consultas Após Diagnóstico de Câncer

Este gráfico combinado mostra a média de dias acumulados após o diagnóstico de câncer e a distribuição de pessoas ao longo das consultas. As barras representam a quantidade de pessoas em cada número de consultas, enquanto a linha indica a média de dias acumulados.
"""

descricao_analise_cids = """
### Análise de CID

Esta tabela fornece uma análise detalhada dos CIDs, incluindo a frequência de cada CID, a porcentagem de pacientes que tiveram pelo menos uma consulta com aquele CID, a média de dias para ter a consulta daquele CID e a média do número da consulta daquele CID.
"""

# Configuração do Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Análises do Projeto Oncoclínicas"),
    html.Hr(),
    
    html.Div([
        dcc.Markdown(descricao_distribuicao_sexo_idade),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2)
    ]),
    
    html.Div([
        dcc.Markdown(descricao_distribuicao_cids),
        dcc.Graph(figure=fig3)
    ]),
    
    html.Div([
        dcc.Markdown(descricao_media_dias_consultas),
        dcc.Graph(figure=fig4)
    ]),
    
    html.Div([
        dcc.Markdown(descricao_analise_cids),
        dcc.Graph(figure=fig5)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
