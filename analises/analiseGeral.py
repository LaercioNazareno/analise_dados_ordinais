import pandas as pd
from scipy.stats import kendalltau
from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans

class AnaliseGeral:
    def __init__(self) -> None:
        self.df = pd.read_csv('./dados/dados_tratados.csv')
        self.df_intersecao = pd.read_csv('./dados/dados_intersecao.csv')
        self.df_completo = pd.merge(self.df, self.df_intersecao, on='id')
        self.df_selecionado = self.df
    
    def alterar_df(self, df):
        self.df_selecionado = df
    
    def buscar_colunas(self):
        colunas = list(self.df_selecionado.columns)
        colunas.pop(0)
        return colunas
    
    def buscar_colunas_numericas(self):
        return self.df_selecionado.select_dtypes(include='number').columns
    
    def buscar_colunas_texto(self):
        return self.df_selecionado.select_dtypes(include=['object']).columns
    
    def buscar_valores_distintos_coluna(self, coluna):
        return self.df_selecionado[coluna].unique()
    
    def buscar_valores_colunas(self, coluna):
        return self.df_selecionado[coluna]
    
    def buscar_qtd_dados(self):
        return len(self.df_selecionado)
    
    def buscar_dados_agrupados_filtrado_por(self, filtros):
        df = self.df_selecionado
        campos = []
        for filtro in filtros:
            campos.append(filtro['campo'])
            df = df[df[filtro['campo']] == filtro['valor']]
        df = df.groupby(campos).size().reset_index(name='quantidade')
        df['porcentagem'] = (df['quantidade'] / self.buscar_qtd_dados()) * 100
        
        categorias = []
        for index, row in df.iterrows():
            categoria = ''
            for campo in campos:
                categoria = categoria + ' ' + str(row[campo])
            categorias.append(categoria)
        
        df['categoria'] = categorias
        return df
    
    def buscar_dados_agrupados_por(self, campos: list):
        dados_agrupados = self.df_selecionado.groupby(campos).size().reset_index(name='quantidade')
        dados_agrupados['porcentagem'] = (dados_agrupados['quantidade'] / self.buscar_qtd_dados()) * 100
        
        categorias = []
        for index, row in dados_agrupados.iterrows():
            categoria = ''
            for campo in campos:
                categoria = categoria + ' ' + str(row[campo])
            categorias.append(categoria)
        
        dados_agrupados['categoria'] = categorias
        return dados_agrupados
        
    def buscar_correlacao(self, colunas):
        coorelacao = self.df_selecionado[colunas].corr(method='kendall').stack().reset_index().rename(columns={0: 'correlation'})
        coorelacao['correlation_label'] = coorelacao.iloc[:, [2]].map('{:.2f}'.format)
        return coorelacao
    
    def buscar_correlacao_acima_de(self, valor):
        df_correlacao = self.df_selecionado[self.buscar_colunas_numericas()]
        correlacao = df_correlacao.corr(method='kendall').stack().reset_index().rename(columns={0: 'correlation'})
        correlacao['correlation_label'] = correlacao.iloc[:, [2]].map('{:.2f}'.format)
        return correlacao[correlacao['correlation'] > valor] 
    
    def calculate_wcss(self, df_encoded):
        range_k = range(2, 30)
        lista_sse = []
        lista_k = []

        for k in range_k:
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(df_encoded)
            lista_sse.append(kmeans.inertia_)
            lista_k.append(k)
        k_ideal = lista_k[lista_sse.index(min(lista_sse))]
        df_qt_clusters = pd.DataFrame({'k': lista_k, 'SSE': lista_sse})
        return df_qt_clusters, k_ideal
    
    def determinar_clusters(self, colunas):
        encoder = OrdinalEncoder()
        df_encoded = encoder.fit_transform(self.df_selecionado[colunas])
        df_qt_clusters, k_ideal = self.calculate_wcss(df_encoded)
        return df_qt_clusters, k_ideal
    
    def clusterizar(self, n_clusters, colunas):
        encoder = OrdinalEncoder()
        df_encoded = encoder.fit_transform(self.df_selecionado[colunas])
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(df_encoded)
        return kmeans.labels_

    def correlacionar(self, campos):
        campo_1 = campos[0]
        campo_2 = campos[1]
        corr, p_value = kendalltau(self.df_selecionado[campo_1], self.df_selecionado[campo_2])
        return corr, p_value
    
    def set_list(self, campo_1, campo_2):
        return list(set([campo_1,campo_2]))
    
    def add_campos_numericos(self, campo_1, campo_2):
        campo_3 = campo_1 + '_Numerico'
        campo_4 = campo_2 + '_Numerico'
        return list(set([campo_1, campo_2, campo_3, campo_4]))
    
    def buscar_valores_completo_distintos_coluna(self, coluna):
        return self.df_completo[coluna].unique()
    
    def valores_filtrados_resposta(self, campo_resposta):
        dados_agrupados = self.df_completo[self.df_completo['frequentemente_tem_estresse_ansiedade'].isin(campo_resposta)]
        ids = dados_agrupados['id'].unique()
        return self.df[self.df['id'].isin(ids)]
    