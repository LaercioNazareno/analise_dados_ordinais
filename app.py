import altair as alt
import streamlit as st
from analises.analiseGeral import AnaliseGeral

## Criação da analise
analise_geral = AnaliseGeral()

st.title('Analise')
st.subheader('Avaliar dados pelo conjunto')
st.write('(pergunta Quem é responsável por custear os seus estudos)')
campo_resposta = st.multiselect("Selecione campos resposta para analise população", analise_geral.buscar_valores_completo_distintos_coluna('resposta'))
if len(campo_resposta) > 0:
    dados_resposta = analise_geral.valores_filtrados_resposta(campo_resposta)
    st.dataframe(dados_resposta)
    analise_geral.alterar_df(dados_resposta)

st.subheader('Inicio das analises')

st.write(f'total de respostas: {analise_geral.buscar_qtd_dados()}')

## Gerar graficos de barras:
campo = st.selectbox("Selecione um campo", analise_geral.buscar_colunas_texto())
dados = analise_geral.buscar_dados_agrupados_por([campo])

# Exibindo o gráfico no Streamlit
bar_chart = alt.Chart(dados).mark_bar().encode(
    x=alt.X('quantidade', title='quantidade'),
    y=alt.Y(campo, title=campo, sort='-x'),
    color=campo
).properties(
    title=f'Gráfico de Barras: {campo}'
)
st.altair_chart(bar_chart, use_container_width=True)

## Gerar tablea
st.table(dados)

## Correlação
st.subheader('Correlação')

st.write('Todas as variaveis')
valor_correlacao = st.number_input("buscar dados correlatos acima de:")
dados_correlatos = analise_geral.buscar_correlacao_acima_de(valor_correlacao)
chart_heatmap = alt.Chart(dados_correlatos).mark_rect().encode(
    x='level_0',
    y='level_1',
    color='correlation',
    text='correlation_label'
)
st.altair_chart(chart_heatmap, use_container_width=True)

st.write('correlação com variaveis selecionadas')
campos_correlacao = st.multiselect("Selecione campos correlacao", analise_geral.buscar_colunas_numericas())
if len(campos_correlacao) > 1:
    correlacao = analise_geral.buscar_correlacao(campos_correlacao)
    chart_heatmap = alt.Chart(correlacao).mark_rect().encode(
        x='level_0',
        y='level_1',
        color='correlation',
        text='correlation_label'
    )
    st.altair_chart(chart_heatmap, use_container_width=True)
    
st.subheader("Relação entre os dados")
campos_geracao = st.selectbox("Selecione variavel para geracao do grafico", analise_geral.buscar_colunas_texto())
campos_comparacao = st.selectbox("Selecione campos para comparacao", analise_geral.buscar_colunas_texto())
campos = analise_geral.set_list(campos_geracao, campos_comparacao)
if len(campos) > 1:
    df = analise_geral.buscar_dados_agrupados_por(list(campos))
    corr, p_value = analise_geral.correlacionar(list(campos))
    st.write(f'O nivel de significancia(p valor) é de {round(p_value,2)} com uma correlação de {round(corr,2)}')
    st.table(df)
    for item in df[campos_geracao].unique():
        df_filter = df[df[campos_geracao] == item]
        
        bar_chart = alt.Chart(df_filter).mark_bar().encode(
        x=alt.X('quantidade', title='quantidade'),
        y=alt.Y(campos_comparacao, title=campos_comparacao, sort='-x'),
        color=campos_comparacao
        ).properties(
            title=f'Gráfico de Barras: {item}'
        )
        st.altair_chart(bar_chart, use_container_width=True)

campos_multivariados = st.multiselect("Selecione variaveis para verificar os grupos", analise_geral.buscar_colunas_texto())
if len(campos_multivariados) > 1:
    df = analise_geral.buscar_dados_agrupados_por(list(campos_multivariados))
    st.dataframe(df)
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('quantidade', title='quantidade'),
        y=alt.Y('categoria', title=campo, sort='-x'),
        color='categoria'
    ).properties(
        title=f'Gráfico de Barras: {campo}'
    )
    st.altair_chart(bar_chart, use_container_width=True)

st.subheader('Classificação')
campos_clusterizacao = st.multiselect("Selecione dois campos para classificacao", analise_geral.buscar_colunas_numericas())
if len(campos_clusterizacao) == 2:
    dados_clusterizar = analise_geral.buscar_valores_colunas(campos_clusterizacao)
    
    df_qt_clusters, k_ideal = analise_geral.determinar_clusters(campos_clusterizacao)
    st.write('Tecnica do cotovelo para determiar a quantidade de agrupamentos')
    
    grafico_cotovelo = alt.Chart(df_qt_clusters).mark_line().encode(
        x='k:Q',
        y='SSE:Q'
    )
    st.altair_chart(grafico_cotovelo)
    qtd_cluster = st.number_input("Selecione o valores no meio da curvatura do grafico acima", min_value=1)
    clusters = analise_geral.clusterizar(qtd_cluster, campos_clusterizacao)
    dados_clusterizar['clusters'] = clusters
    
    grafico_pontos = alt.Chart(dados_clusterizar).mark_point().encode(
        x=campos_clusterizacao[0],
        y=campos_clusterizacao[1],
        color='clusters:N'
    )
    
    st.altair_chart(grafico_pontos, use_container_width=True)
    nome_coluna_1 = campos_clusterizacao[0].replace('_Numerico', '')
    legenda_1 = analise_geral.buscar_valores_distintos_coluna(nome_coluna_1)
    st.write(nome_coluna_1)
    for i in range(len(legenda_1)):
        st.write(str((i + 1)) +" = " + str(legenda_1[i]))
    
    nome_coluna_2 = campos_clusterizacao[1].replace('_Numerico', '')
    legenda_2 = analise_geral.buscar_valores_distintos_coluna(nome_coluna_2)
    st.write(nome_coluna_2)
    for i in range(len(legenda_2)):
        st.write(str((i + 1)) +" = " + str(legenda_2[i]))
