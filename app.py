import altair as alt
import streamlit as st
from analises.analiseGeral import AnaliseGeral
import seaborn as sns
import matplotlib.pyplot as plt

## Criação da analise
analise_geral = AnaliseGeral()

st.title('Analise')
st.subheader('Avaliação de dados ordinais')

st.write(f'total de respostas: {analise_geral.buscar_qtd_dados()}')

## Gerar graficos de barras:
campo = st.selectbox("Selelcione um campo", analise_geral.buscar_colunas())
dados = analise_geral.buscar_dados_agrupados_por(campo)

st.subheader(f'{campo}')

# Exibindo o gráfico no Streamlit
bar_chart = alt.Chart(dados).mark_bar().encode(
    x=alt.X('quantidade', title='quantidade'),
    y=alt.Y(campo, title=campo, sort='-x')
).properties(
    title=f'Gráfico de Barras: {campo}'
)
st.altair_chart(bar_chart, use_container_width=True)

## Gerar tablea
st.table(dados)

## Diagrama de venn
st.subheader("Relação entre os dados")
campos = st.multiselect("Selecione as variaveis a ser analisadas", analise_geral.buscar_colunas())
if campos:
    corr, p_valor = analise_geral.correlacionar(campos)
    st.write(f'As variaveis tem um grau de significancia de {round(p_valor,4)} e uma correlação de {round(corr,4)}')
    dados_compostos = analise_geral.buscar_dados_agrupados_por(campos)
    st.table(dados_compostos)

## Correlação
st.subheader('Correlação')
campos_correlacao = st.multiselect("Selecione campos correlacao", analise_geral.buscar_colunas_numericas())
if campos_correlacao:
    correlacao = analise_geral.buscar_correlacao(campos_correlacao)
    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    sns.heatmap(correlacao, ax=ax)
    st.write(fig)

## Clusterização
st.subheader('Classificacao')

# campos_correlacao = st.multiselect("Selecione campos para classificacao", analise_geral.buscar_colunas_numericas())
# if campos_correlacao:
#     max_clusters = int(st.number_input("Quantidade maxima de clusters", min_value=1))
#     if max_clusters > 0:
#         wcss = analise_geral.determinar_clusters(max_clusters, campos_correlacao)

#         plt.figure(figsize=(10, 5))
#         plt.plot(range(1, max_clusters + 1), wcss, 'bo-')
#         plt.xlabel('Número de Clusters')
#         plt.ylabel('WCSS')
#         plt.title('Técnica do Cotovelo para Determinação do Número de Clusters')
#         st.pyplot(plt)

#     num_clusters = int(st.number_input("Quantidade de clusters", min_value=1))
#     df_encoded, clusters = analise_geral.clusterizar(num_clusters, campos_correlacao)
#     st.dataframe(df_encoded)
#     plt.figure(figsize=(10, 5))
#     sns.scatterplot(x=df_encoded[:, 0], y=df_encoded[:, 1], hue=clusters, palette='viridis', s=100)
#     plt.title('Clusters K-Medoids')
#     plt.xlabel(f'{campos_correlacao[0]}')
#     plt.ylabel(f'{campos_correlacao[1]}')
#     st.pyplot(plt)