import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurações de Estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def analise_especialista_voos(path_flights, path_airports, path_airlines):
    # 1. CARREGAMENTO E LIMPEZA
    cols_of_interest = [
        'MONTH', 'DAY_OF_WEEK', 'AIRLINE', 'ORIGIN_AIRPORT', 
        'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 
        'SCHEDULED_DEPARTURE', 'DISTANCE', 'CANCELLED'
    ]
    
    df = pd.read_csv(path_flights, usecols=cols_of_interest)
    airports = pd.read_csv(path_airports)
    airlines = pd.read_csv(path_airlines)

    # Tratamento de Nulos: Voos cancelados não têm atraso. 
    df_clean = df[df['CANCELLED'] == 0].copy()
    df_clean['DEPARTURE_DELAY'] = df_clean['DEPARTURE_DELAY'].fillna(0)
    df_clean['ARRIVAL_DELAY'] = df_clean['ARRIVAL_DELAY'].fillna(0)

    # 2. ESTATÍSTICAS DESCRITIVAS GERAIS
    print("--- Estatísticas de Atraso (Minutos) ---")
    print(df_clean[['DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'DISTANCE']].describe())

    # Agrupamos por aeroporto de origem e calculamos a média de atraso
    atraso_aeroporto = df_clean.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().sort_values(ascending=False).head(10)
    atraso_aeroporto = atraso_aeroporto.reset_index().merge(airports[['IATA_CODE', 'AIRPORT']], left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')

    # Analisamos Correlação e Atraso por Distância
    df_clean['faixa_distancia'] = pd.qcut(df_clean['DISTANCE'], q=4, labels=['Curta', 'Média-Curta', 'Média-Longa', 'Longa'])
    atraso_distancia = df_clean.groupby('faixa_distancia')['DEPARTURE_DELAY'].mean()

    # Extrair hora do SCHEDULED_DEPARTURE (Formato HHMM)
    df_clean['HOUR'] = df_clean['SCHEDULED_DEPARTURE'] // 100
    atraso_hora = df_clean.groupby('HOUR')['DEPARTURE_DELAY'].mean()
    atraso_dia = df_clean.groupby('DAY_OF_WEEK')['DEPARTURE_DELAY'].mean()

    # --- VISUALIZAÇÕES ---

    # Gráfico 1: Atraso por Hora do Dia
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=atraso_hora.index, y=atraso_hora.values, marker='o', color='darkblue')
    plt.title('Evolução do Atraso Médio ao Longo do Dia')
    plt.xticks(range(0, 24))
    plt.xlabel('Hora do Dia (Partida Programada)')
    plt.ylabel('Atraso Médio (Minutos)')
    plt.show()

    # Gráfico 2: Atraso por Dia da Semana
    dias = {1:'Seg', 2:'Ter', 3:'Qua', 4:'Qui', 5:'Sex', 6:'Sáb', 7:'Dom'}
    plt.figure(figsize=(10, 5))
    sns.barplot(x=[dias[i] for i in atraso_dia.index], y=atraso_dia.values, palette='Blues_d')
    plt.title('Atraso Médio por Dia da Semana')
    plt.ylabel('Minutos')
    plt.show()

# Execução (ajuste os nomes dos arquivos conforme necessário)
analise_especialista_voos('flights.csv', 'airports.csv', 'airlines.csv')