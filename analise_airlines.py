import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# 1. Configuração de Estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def executar_eda_airlines(caminho_arquivo):
    # --- CARREGAMENTO DOS DADOS ---
    try:
        df = pd.read_csv(caminho_arquivo)
        print("✅ Dados carregados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar o arquivo: {e}")
        return

    # --- 2. INSPEÇÃO INICIAL E ESTATÍSTICAS ---
    print("\n--- Estrutura dos Dados ---")
    print(df.info())
    
    print("\n--- Primeiras Linhas ---")
    print(df.head())

    # Verificação de Valores Ausentes
    print("\n--- Valores Ausentes ---")
    missing = df.isnull().sum()
    print(missing)

    # Vamos extrair métricas dos nomes das companhias para análise
    df['nome_comprimento'] = df['AIRLINE'].apply(len)
    df['qtd_palavras'] = df['AIRLINE'].apply(lambda x: len(x.split()))

    print("\n--- Estatísticas Descritivas (Nomes) ---")
    print(df[['nome_comprimento', 'qtd_palavras']].describe())

    # Nota: Este dataset específico não possui nulos, mas o código abaixo trata casos futuros
    if df.isnull().values.any():
        # Para dados categóricos como estes, preencheríamos com 'Unknown' ou removeríamos
        df = df.dropna() 
        print("\n⚠️ Valores ausentes removidos.")
    else:
        print("\n✔️ Nenhum valor ausente detectado.")

    # --- 5. ANÁLISE DE FREQUÊNCIA DE PALAVRAS ---
    todas_palavras = []
    for nome in df['AIRLINE']:
        palavras = re.findall(r'\w+', nome)
        todas_palavras.extend(palavras)

    contagem_palavras = Counter(todas_palavras).most_common(10)
    df_palavras = pd.DataFrame(contagem_palavras, columns=['Palavra', 'Frequência'])

    # --- 6. VISUALIZAÇÕES ---
    
    # Gráfico 1: Comprimento dos Nomes
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='nome_comprimento', 
        y='AIRLINE', 
        data=df.sort_values('nome_comprimento', ascending=False),
        palette='viridis'
    )
    plt.title('Análise de Tamanho do Nome das Companhias Aéreas', fontsize=15)
    plt.xlabel('Número de Caracteres')
    plt.ylabel('Companhia Aérea')
    plt.tight_layout()
    plt.show()

    # Gráfico 2: Palavras mais comuns
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='Frequência', 
        y='Palavra', 
        data=df_palavras, 
        palette='magma'
    )
    plt.title('Top 10 Termos mais Frequentes nos Nomes', fontsize=15)
    plt.xlabel('Contagem de Ocorrências')
    plt.ylabel('Termo')
    plt.tight_layout()
    plt.show()

    return df

# Executar a função
# Substitua 'airlines.csv' pelo caminho real se estiver no seu computador local
df_final = executar_eda_airlines('airlines.csv')