import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def executar_clusterizacao():
    print("--- 1. Carregando dados para Clusterização ---")
    try:
        # Carrega os dados de voos
        df = pd.read_csv('flights.csv', usecols=['ORIGIN_AIRPORT', 'DEPARTURE_DELAY'], low_memory=False)
        
        # Agrupa por aeroporto e calcula média e contagem
        stats = df.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].agg(['mean', 'count']).dropna()
        stats.columns = ['atraso_medio', 'total_voos']
        
        # Filtra aeroportos com mais de 1000 voos para limpar o gráfico
        stats = stats[stats['total_voos'] > 1000]
        print(f"✅ Analisando {len(stats)} aeroportos principais.")

        # --- 2. K-Means ---
        # Dividindo em 3 grupos: Pequeno atraso, Médio e Crítico
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        stats['cluster'] = kmeans.fit_predict(stats[['atraso_medio', 'total_voos']])

        # --- 3. Visualização ---
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=stats, x='total_voos', y='atraso_medio', hue='cluster', palette='Set1', s=100)
        
        # Anotações seguras usando .iloc
        for i in range(min(20, len(stats))):
            plt.annotate(stats.index[i], 
                         (stats['total_voos'].iloc[i], stats['atraso_medio'].iloc[i]),
                         xytext=(5, 5), textcoords='offset points', fontsize=8)

        plt.title('Clusterização de Aeroportos: Eficiência vs. Volume (Tech Challenge)')
        plt.xlabel('Volume de Voos (Total)')
        plt.ylabel('Média de Atraso na Partida (Minutos)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
        
        print("✅ Gráfico gerado com sucesso! Salve esta imagem para sua apresentação.")

    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")

if __name__ == "__main__":
    executar_clusterizacao()