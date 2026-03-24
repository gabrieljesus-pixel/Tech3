import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configurações de exibição e estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 7)

def analisar_aeroportos(caminho_arquivo):
    # --- CARREGAMENTO ---
    df = pd.read_csv('C:\\Users\\DELL CORE i7\\Desktop\\Machine Learning\\Tech3\\airports.csv')
    print(f"✅ Dataset carregado: {df.shape[0]} linhas e {df.shape[1]} colunas.")

    # --- 2. TRATAMENTO DE VALORES AUSENTES ---
    # Identificando nulos
    nulos = df.isnull().sum()
    print("\n--- Valores Ausentes Identificados ---")
    print(nulos[nulos > 0])

    # No caso de coordenadas geográficas, se forem poucos (ex: 3 de 322), 
    # a melhor prática para EDA é remover essas linhas para não distorcer mapas.
    df_clean = df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
    print(f"\n✔️ Tratamento: {df.isnull().any(axis=1).sum()} linhas com nulos removidas.")

    # --- 3. ESTATÍSTICAS DESCRITIVAS ---
    print("\n--- Estatísticas Categóricas ---")
    # Quantos estados e cidades únicos?
    print(df_clean[['CITY', 'STATE', 'COUNTRY']].describe())

    # --- 4. VISUALIZAÇÕES E INSIGHTS ---
    
    # Insights 1: Distribuição por Estado
    plt.figure(figsize=(15, 6))
    state_counts = df_clean['STATE'].value_counts().sort_values(ascending=False)
    sns.barplot(x=state_counts.index, y=state_counts.values, palette='viridis')
    plt.title('Distribuição de Aeroportos por Estado (EUA)', fontsize=16)
    plt.xlabel('Estado')
    plt.ylabel('Quantidade de Aeroportos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Insight 2: Localização Geográfica (Mapa Simples)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df_clean, 
        x='LONGITUDE', 
        y='LATITUDE', 
        hue='STATE', 
        legend=False, 
        alpha=0.6,
        palette='tab20'
    )
    plt.title('Distribuição Geográfica dos Aeroportos', fontsize=16)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Anotação para destacar áreas como Alasca (AK) que costumam ficar isoladas
    plt.annotate('Alasca', xy=(-150, 60), xytext=(-160, 65),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.tight_layout()
    plt.show()

    # Insight 3: Comprimento dos nomes dos Aeroportos
    df_clean['nome_len'] = df_clean['AIRPORT'].apply(len)
    plt.figure(figsize=(10, 5))
    sns.histplot(df_clean['nome_len'], bins=20, kde=True, color='skyblue')
    plt.title('Distribuição do Tamanho do Nome dos Aeroportos', fontsize=16)
    plt.xlabel('Número de Caracteres')
    plt.ylabel('Frequência')
    plt.show()

    return df_clean

# Execução do script
if __name__ == "__main__":
    # Certifique-se que o arquivo 'airports.csv' está na mesma pasta
    df_final = analisar_aeroportos('airports.csv')