# Tech3
TechChalenge Fiap
# Tech Challenge - Fase 3 - Machine Learning Engineering

Sobre o Projeto
Este projeto analisa dados de voos dos EUA para prever e agrupar atrasos utilizando Machine Learning.

Estrutura de Arquivos
- `analise_flights.py`: EDA principal e tratamento de dados.
- `analise_aeroporto.py` & `analise_airlines.py`: Exploração de entidades.
- `modelagem_supervisionada.py`: Comparação entre Regressão Logística e Random Forest.
- `clusterizacao_aeroportos.py`: Agrupamento de aeroportos via K-Means.

## Como rodar
1. Instale as dependências: `pip install pandas scikit-learn seaborn`
2. Execute os scripts de análise primeiro e depois os de modelagem.

## Principais Conclusões
- O modelo Random Forest com `class_weight='balanced'` obteve um Recall de 65% para atrasos.
- Identificamos 3 clusters principais de aeroportos baseados em volume e eficiência.

- ## Observação - Flights:
- Dado que o arquivo flights.csv excede a capacidade de hospedagem do github, segue link para download da base:
- https://drive.google.com/file/d/1pBlOhZxXzb1ybAc9hDCi9OX0hOFI8X0z/view?usp=sharing
