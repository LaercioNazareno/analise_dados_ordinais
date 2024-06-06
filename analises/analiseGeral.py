import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from sklearn.preprocessing import OrdinalEncoder
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import pairwise_distances

class AnaliseGeral:
    def __init__(self) -> None:
        self.df = pd.read_csv('./dados/dados_tratados.csv')
    
    def buscar_colunas(self):
        colunas = list(self.df.columns)
        colunas.pop(0)
        return colunas
    
    def buscar_valores_coluna(self, coluna):
        return self.df[coluna].unique()
    
    def buscar_qtd_dados(self):
        return len(self.df)
        
    def buscar_dados_agrupados_por(self, campos):
        dados_agrupados = self.df.groupby(campos).size().reset_index(name='quantidade')
        dados_agrupados['poecentagem'] = round((dados_agrupados['quantidade'] / self.buscar_qtd_dados()) * 100, 2)
        return dados_agrupados
    
    def buscar_colunas_numericas(self):
        return self.df.select_dtypes(include='number').columns
    
    def buscar_correlacao(self, colunas):
        return self.df[colunas].corr(method='kendall')
    
    def calculate_wcss(self, df_encoded, max_clusters):
        wcss = []
        dist_matrix = pairwise_distances(df_encoded, metric='manhattan')
        for n in range(1, max_clusters + 1):
            kmedoids = KMedoids(n_clusters=n, metric='precomputed', random_state=42)
            kmedoids.fit(dist_matrix)
            wcss.append(kmedoids.inertia_)
        return wcss
    
    def determinar_clusters(self, max_clusters, colunas):
        encoder = OrdinalEncoder()
        df_encoded = encoder.fit_transform(self.df[colunas])
        wcss = self.calculate_wcss(df_encoded, max_clusters)
        return wcss
    
    def clusterizar(self, n_clusters, colunas):
        encoder = OrdinalEncoder()
        df_encoded = encoder.fit_transform(self.df)
        dist_matrix = pairwise_distances(df_encoded, metric='manhattan')
        kmedoids = KMedoids(n_clusters=n_clusters, metric='precomputed', random_state=42)
        clusters = kmedoids.fit_predict(dist_matrix)
        return df_encoded, clusters

    def correlacionar(self, campos):
        campo_1 = campos[0]
        campo_2 = campos[1]
        corr, p_value = kendalltau(self.df[campo_1], self.df[campo_2])
        return corr, p_value